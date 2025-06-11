"""
Create a test PDF file using PyMuPDF.
"""
import fitz
import os

def create_test_pdf():
    # Create a new PDF document
    doc = fitz.open()
    
    # Add a page
    page = doc.new_page()
    
    # Define text content
    title = "Test PDF Document"
    content = """
    This is a test PDF document created for debugging purposes.
    
    It contains multiple paragraphs of text to test the PDF processing functionality.
    
    The text should be properly extracted and chunked by the application.
    
    This document will help verify that:
    1. PDF upload works correctly
    2. Text extraction is functioning
    3. Chunking process is working
    4. Embeddings can be generated
    5. Storage in ChromaDB is successful
    """
    
    # Insert title
    page.insert_text((50, 50), title, fontsize=16, fontname="helv-b")
    
    # Insert content
    page.insert_text((50, 100), content, fontsize=12, fontname="helv")
    
    # Save the PDF
    output_path = "test.pdf"
    doc.save(output_path)
    doc.close()
    
    print(f"Test PDF created successfully at {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_test_pdf() 