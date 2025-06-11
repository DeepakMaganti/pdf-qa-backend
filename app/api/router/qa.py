from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from typing import List
import os

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/query", response_model=QueryResponse)
async def query_pdf(query: QueryRequest):
    try:
        # Read the latest uploaded PDF filename
        if not os.path.exists("latest_pdf.txt"):
            raise HTTPException(status_code=400, detail="No PDF has been uploaded yet.")
        with open("latest_pdf.txt", "r") as f:
            pdf_id = f.read().strip()
        if not pdf_id:
            raise HTTPException(status_code=400, detail="No PDF has been uploaded yet.")
        # Load vector store for the latest PDF
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        vectordb = Chroma(
            persist_directory=settings.CHROMA_DB_DIR,
            embedding_function=embeddings,
            collection_name=pdf_id
        )
        retriever = vectordb.as_retriever(search_kwargs={"k": 5})
        llm = ChatOpenAI(model_name="gpt-4", openai_api_key=settings.OPENAI_API_KEY)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        result = qa_chain({"query": query.question})
        answer = result["result"]
        sources = [doc.page_content for doc in result["source_documents"]]
        return QueryResponse(answer=answer, sources=sources)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 