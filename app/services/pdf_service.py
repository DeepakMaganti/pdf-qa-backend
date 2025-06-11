import os
from app.core.config import settings
from app.services.pdf_parser import parse_pdf
from app.services.chunking import split_text_into_chunks
from app.services.embedding import embed_chunks
from app.services.vector_store import add_chunks_and_embeddings
import chromadb
from chromadb.config import Settings as ChromaSettings

class PDFService:
    def __init__(self):
        self.client = chromadb.Client(ChromaSettings(
            persist_directory=settings.CHROMA_DIR
        ))
        self.collection = self.client.get_or_create_collection("pdfs")

    async def process_pdf(self, file_path: str) -> dict:
        """
        Process a PDF file and store its content in the vector database
        """
        try:
            # Extract text from PDF using the shared utility
            text = parse_pdf(file_path)
            # Split text into chunks using the shared utility
            chunks = split_text_into_chunks(text)
            # Generate embeddings for the chunks
            embeddings = embed_chunks(chunks)
            # Prepare metadata
            metadatas = [{"source": file_path, "chunk_index": i} for i in range(len(chunks))]
            # Store chunks and embeddings in vector database
            add_chunks_and_embeddings(chunks, embeddings, metadatas)
            return {"status": "success", "chunks": len(chunks)}
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def list_processed_pdfs(self) -> list:
        """
        List all processed PDFs
        """
        try:
            # Get unique PDF filenames from the collection
            results = self.collection.get()
            unique_sources = set()
            for metadata in results["metadatas"]:
                unique_sources.add(metadata["source"])
            return list(unique_sources)
        except Exception as e:
            raise Exception(f"Error listing PDFs: {str(e)}") 