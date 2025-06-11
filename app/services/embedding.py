import openai
from typing import List
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)
openai.api_key = settings.OPENAI_API_KEY

def embed_chunks(texts: List[str], model: str = "text-embedding-3-small") -> List[list]:
    try:
        logger.info(f"Generating embeddings for {len(texts)} chunks using model {model}")
        response = openai.Embedding.create(
            input=texts,
            model=model
        )
        embeddings = [item['embedding'] for item in response['data']]
        logger.info(f"Successfully generated {len(embeddings)} embeddings")
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise 