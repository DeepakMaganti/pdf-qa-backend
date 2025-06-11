"""
Text chunking utilities for splitting text into manageable chunks.
"""
from typing import List
import logging

logger = logging.getLogger(__name__)

def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks of specified size.
    
    Args:
        text: Text to split into chunks
        chunk_size: Maximum size of each chunk (default: 500)
        overlap: Number of characters to overlap between chunks (default: 50)
        
    Returns:
        List of text chunks
    """
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
            
        if chunk_size <= 0 or overlap < 0:
            raise ValueError("chunk_size must be positive and overlap must be non-negative")
            
        if overlap >= chunk_size:
            raise ValueError("overlap must be less than chunk_size")
        
        chunks = []
        start = 0
        text_length = len(text)
        
        logger.info(f"Splitting text of length {text_length} into chunks of size {chunk_size}")
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            # If we're not at the end of the text, try to find a good break point
            if end < text_length:
                # Look for the last period or newline in the chunk
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                split_point = max(last_period, last_newline)
                
                if split_point != -1:
                    end = split_point + 1
                else:
                    # If no good break point found, try to break at a space
                    last_space = text.rfind(' ', start, end)
                    if last_space != -1:
                        end = last_space + 1
            
            # Extract the chunk and clean it
            chunk = text[start:end].strip()
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)
            
            # Move the start pointer, accounting for overlap
            start = max(start + 1, end - overlap)
        
        logger.info(f"Successfully split text into {len(chunks)} chunks")
        return chunks
        
    except Exception as e:
        logger.error(f"Error in split_text_into_chunks: {str(e)}")
        raise 