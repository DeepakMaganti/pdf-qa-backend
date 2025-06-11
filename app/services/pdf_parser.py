"""
PDF parsing utilities using PyMuPDF.
"""
import fitz  # PyMuPDF
import io
from typing import Union
import logging

logger = logging.getLogger(__name__)

def parse_pdf(input_data: Union[str, bytes]) -> str:
    """
    Parse PDF content from either a file path or bytes using PyMuPDF.
    
    Args:
        input_data: Either a file path (str) or PDF content (bytes)
        
    Returns:
        Extracted text from the PDF
        
    Raises:
        ValueError: If the input is invalid or PDF is corrupted
        Exception: For other unexpected errors
    """
    try:
        if isinstance(input_data, str):
            # Handle file path
            logger.info(f"Reading PDF from file: {input_data}")
            doc = fitz.open(input_data)
        else:
            # Handle bytes
            logger.info("Reading PDF from bytes")
            doc = fitz.open(stream=input_data, filetype="pdf")
        
        # Validate PDF
        if doc.page_count == 0:
            raise ValueError("PDF file is empty")
        
        # Extract text from each page
        texts = []
        for i, page in enumerate(doc):
            try:
                # Get text with better formatting
                text = page.get_text("text")
                if text:
                    texts.append(text)
                else:
                    logger.warning(f"No text extracted from page {i+1}")
            except Exception as e:
                logger.warning(f"Error extracting text from page {i+1}: {str(e)}")
        
        # Close the document
        doc.close()
        
        if not texts:
            raise ValueError("No text could be extracted from the PDF")
        
        # Join all text with newlines
        full_text = "\n".join(texts)
        logger.info(f"Successfully extracted {len(texts)} pages of text")
        return full_text
        
    except ValueError as ve:
        logger.error(f"PDF parsing error: {str(ve)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error parsing PDF: {str(e)}")
        raise
