"""
ChromaDB vector store utilities.
"""
import chromadb
from typing import List, Dict, Tuple
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
collection = client.get_or_create_collection("pdf_chunks")

# Maximum batch size for ChromaDB
MAX_BATCH_SIZE = 100

def add_chunks_and_embeddings(chunks: List[str], embeddings: List[list], metadatas: List[Dict]):
    """
    Add text chunks and their embeddings to ChromaDB in batches.
    
    Args:
        chunks: List of text chunks
        embeddings: List of embedding vectors
        metadatas: List of metadata dictionaries
    """
    try:
        total_chunks = len(chunks)
        logger.info(f"Adding {total_chunks} chunks to ChromaDB")
        
        # Process in batches
        for i in range(0, total_chunks, MAX_BATCH_SIZE):
            batch_end = min(i + MAX_BATCH_SIZE, total_chunks)
            batch_chunks = chunks[i:batch_end]
            batch_embeddings = embeddings[i:batch_end]
            batch_metadatas = metadatas[i:batch_end]
            batch_ids = [f"chunk_{j}" for j in range(i, batch_end)]
            
            logger.info(f"Adding batch {i//MAX_BATCH_SIZE + 1} ({len(batch_chunks)} chunks)")
            
            collection.add(
                embeddings=batch_embeddings,
                documents=batch_chunks,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            
        logger.info("Successfully added all chunks to ChromaDB")
        
    except Exception as e:
        logger.error(f"Error adding chunks to ChromaDB: {str(e)}")
        raise

def query_similar_chunks(query_embedding: list, top_k: int = 5) -> List[Tuple[str, Dict]]:
    """
    Query ChromaDB for similar chunks using an embedding vector.
    
    Args:
        query_embedding: Query embedding vector
        top_k: Number of similar chunks to return
        
    Returns:
        List of (chunk, metadata) tuples
    """
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return list(zip(results["documents"][0], results["metadatas"][0]))
    except Exception as e:
        logger.error(f"Error querying ChromaDB: {str(e)}")
        raise

def reset_vector_store():
    try:
        collection.delete()
        logger.info("Vector store reset successfully.")
    except Exception as e:
        logger.error(f"Error resetting vector store: {str(e)}")
        raise 