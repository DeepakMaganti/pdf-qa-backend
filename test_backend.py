import requests
import os
from pathlib import Path
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_PDF_PATH = "test.pdf"  # You'll need to provide a test PDF file

def test_health():
    """Test if the server is running and responding"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Server is running")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        return False

def test_upload_pdf():
    """Test PDF upload functionality"""
    if not os.path.exists(TEST_PDF_PATH):
        print(f"❌ Test PDF file not found at {TEST_PDF_PATH}")
        return False

    try:
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            
        if response.status_code == 200:
            data = response.json()
            print("✅ PDF upload successful")
            print(f"   - Number of chunks: {data.get('num_chunks')}")
            print(f"   - Preview: {data.get('preview')[:100]}...")
            return True
        else:
            print(f"❌ PDF upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ PDF upload error: {str(e)}")
        return False

def test_ask_question():
    """Test question answering functionality"""
    test_questions = [
        "What is this document about?",
        "Can you summarize the main points?",
        "What are the key findings?"
    ]

    for question in test_questions:
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": question}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Question answered successfully: {question}")
                print(f"   Answer: {data.get('answer')[:100]}...")
            else:
                print(f"❌ Question answering failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Question answering error: {str(e)}")
            return False
    
    return True

def main():
    print("🔍 Testing Backend Functionality")
    print("-" * 50)
    
    # Test server health
    if not test_health():
        return
    
    # Test PDF upload
    if not test_upload_pdf():
        return
    
    # Test question answering
    if not test_ask_question():
        return
    
    print("-" * 50)
    print("✅ All tests completed successfully!")

if __name__ == "__main__":
    main() 