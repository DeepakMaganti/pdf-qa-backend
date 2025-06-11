import pytest
from app.services.embedding import embed_chunks

def test_embedding():
    texts = ["This is a test chunk.", "Another chunk."]
    embeddings = embed_chunks(texts)
    assert len(embeddings) == len(texts)
    assert all(isinstance(vec, list) for vec in embeddings) 