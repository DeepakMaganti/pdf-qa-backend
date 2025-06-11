import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings


from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process PDF
        loader = PyMuPDFLoader(file_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        # Embed and store in Chroma
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        vectordb = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=settings.CHROMA_DB_DIR,
            collection_name=file.filename
        )
        vectordb.persist()

        # Save the latest uploaded PDF filename
        with open("latest_pdf.txt", "w") as f:
            f.write(file.filename)

        return {
            "message": "PDF uploaded and processed successfully",
            "pdf_id": file.filename,
            "preview": chunks[0].page_content[:300] if chunks else "No content extracted.",
            "num_chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/list")
def list_pdfs():
    try:
        files = [f for f in os.listdir(settings.UPLOAD_DIR) if f.endswith('.pdf')]
        return {"pdfs": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
