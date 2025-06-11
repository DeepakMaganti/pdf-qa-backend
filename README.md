# PDF QA Backend

A FastAPI-based backend service for PDF Question Answering using OpenAI and vector search.

## Features

- PDF upload and processing
- Text extraction and chunking
- Vector storage using ChromaDB
- Question answering using OpenAI GPT-4
- RESTful API endpoints

## Project Structure

```
.
├── app/
│   ├── main.py
│   ├── api/
│   │   └── router/
│   │       ├── qa.py
│   │       └── upload.py
│   ├── core/
│   │   └── config.py
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── qa_engine.py
│   │   ├── qa_service.py
│   │   ├── embedding.py
│   │   └── vector_store.py
│   └── __init__.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── data/
│   ├── chroma/
│   └── storage/
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key and storage paths:
```
OPENAI_API_KEY=your_openai_key_here
UPLOAD_DIR=data/storage
CHROMA_DB_DIR=data/chroma
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /` : Serve the frontend
- `GET /api/info` : API welcome message
- `GET /health` : Health check
- `POST /api/upload` : Upload a PDF file
- `GET /api/upload/list` : List all uploaded PDFs
- `POST /api/query` : Ask a question about the most recently uploaded PDF

## Docker

Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `UPLOAD_DIR`: Directory for uploaded PDFs (default: data/storage)
- `CHROMA_DB_DIR`: Directory for ChromaDB persistence (default: data/chroma)

## License
MIT 