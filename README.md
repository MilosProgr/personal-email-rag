# Personal Email RAG System

**Project:** Retrieval-Augmented Generation (RAG) for personal emails and Google Drive documents  
**Author:** Miloš Petković  
**Date:** 2026-03-20  

---

## Overview

This project implements a personal RAG system that enables users to query emails and attached documents (PDF, DOCX, TXT) from Gmail and Google Drive. It combines:

- Vector embeddings (via `sentence-transformers`)  
- Local LLM for generating natural language answers (`bigscience/bloom-560m`)  
- Attachment parsing (PDF, DOCX, TXT)  
- PostgreSQL + `pgvector` for storing embeddings and email metadata  
- Multi-user isolation with per-user authentication tokens  

The system is fully extensible and can be deployed locally using Docker.

---

## Tech Stack

- Python 3.11  
- PostgreSQL + pgvector  
- sentence-transformers  
- Hugging Face Transformers  
- Gmail API & Google Drive API  
- Docker  

---

## Features

✅ Gmail ingestion per user (with OAuth tokens)  
✅ Google Drive ingestion for documents  
✅ Automatic parsing of attachments (.pdf, .docx, .txt)  
✅ Vector database storage with pgvector  
✅ Retrieval of top-K relevant emails/documents  
✅ LLM-powered answer generation based on retrieved content  
✅ Multi-user isolation using per-user authentication tokens  
✅ Metrics for embedding, retrieval, and LLM generation times  

---

## Architecture

The system follows a modular RAG pipeline:

1. **Gmail API / Google Drive API**  
   - Fetches emails and documents per user using OAuth authentication  

2. **Email & Document Parser**  
   - Extracts structured data (sender, subject, body, timestamp)  
   - Parses attachments (PDF, DOCX, TXT)  

3. **Embedding Model**  
   - Converts text into vector representations using sentence-transformers  

4. **Vector Database (pgvector)**  
   - Stores embeddings and metadata  
   - Enables similarity search using vector distance  

5. **RAG Pipeline**  
   - Retrieves top-K relevant documents  
   - Constructs context-aware prompt  

6. **Local LLM**  
   - Generates final answer using retrieved context  

### Design Decisions

- A lightweight embedding model was chosen to ensure fast inference on local hardware.  
- BLOOM-560m was selected as a balance between performance and resource usage.  
- pgvector was used due to its seamless integration with PostgreSQL and efficient similarity search.

### Model Choices

- **Embedding:** all-MiniLM-L6-v2 (fast, lightweight)  
- **LLM:** BLOOM-560m (runs locally, low resource)  
- **DB:** pgvector (efficient similarity search)  

---

## Project Structure

```text
personal-email-rag/
│
├── docs/
│   └── architecture.png        # System architecture diagram
│
├── data/
│   ├── attachments/            # Downloaded Gmail attachments
│   ├── drive_files/            # Downloaded Google Drive files
│   ├── users.json              # User configuration
│   └── credentials.json        # Google OAuth credentials (not included)
│
├── src/
│   ├── attachment_parser.py    # Parses PDF, DOCX, TXT files
│   ├── config.py               # Configuration (DB, models, constants)
│   ├── demo.py                 # Demo script for running queries
│   ├── gmail_client.py         # Gmail & Drive API integration
│   ├── ingest.py               # Data ingestion and embedding pipeline
│   ├── llm_wrapper.py          # Local LLM loading and inference
│   ├── rag_pipeline.py         # Core RAG logic (embed → retrieve → generate)
│   ├── vector_db.py            # PostgreSQL + pgvector operations
│   └── user_auth.py            # Simple user authentication and multi-user validation
│
├── docker-compose.yml          # Docker setup for app + database
├── Dockerfile                  # Docker image for the application
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

```
## Setup
1. Clone repository
git clone <repo_url>
cd personal-email-rag
2. Install dependencies
pip install -r requirements.txt
3. Google credentials

Place your credentials.json in the data/ folder. Do not commit your client secret.

{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "...",
    "token_uri": "...",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
4. Database (PostgreSQL + pgvector)

Use Docker Compose to spin up PostgreSQL with pgvector:

docker-compose up -d

Postgres settings (matches config.py):

Host: localhost

Port: 5440

DB: emails

User: postgres

Password: yourpassword

## Running the Project
1. Ingest emails & files
python src/ingest.py

This will:

Download Gmail messages for all users

Download Google Drive files

Parse attachments

Compute embeddings and insert them into PostgreSQL

2. Run demo queries
python src/demo.py

Example queries:

What did Alice say about the Q4 budget?

Show me emails discussing API integration

Summarize all conversations about the product launch

When did I last hear from the marketing team?

## Usage Notes

User authentication is handled by src/user_auth.py. Only user1 (Alice) and user2 (Bob) are valid by default.

Attachments are automatically parsed using PyPDF2 (PDF), python-docx (DOCX), and plain text reader.

Embeddings are computed using sentence-transformers/all-MiniLM-L6-v2.

Answers are generated using local LLM (bigscience/bloom-560m) to reduce RAM usage.

Metrics are printed for each query:

Embedding: X.XXs | Retrieval: X.XXs | LLM: X.XXs
Docker Setup (Recommended)
Dockerfile (Python app)
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "demo.py"]
docker-compose.yml
version: '3.8'

services:
  db:
    image: ankane/pgvector
    container_name: pgvector-db
    environment:
      POSTGRES_DB: emails
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: yourpassword
    ports:
      - "5440:5432"

  app:
    build: .
    container_name: rag-app
    depends_on:
      - db
    volumes:
      - .:/app

Run docker-compose up to start both DB and app. The app will automatically connect to the DB on localhost:5440.

## Security & Notes

Do NOT commit credentials.json with your Google client secret.

Tokens (token_user1.pkl, token_drive_user1.pkl, etc.) are automatically created per user and stored in data/.

In production, consider parameterized vector queries to prevent SQL injection.

## Limitations

LLM (BLOOM-560m) has limited reasoning capabilities compared to larger models

Gmail API rate limits may affect ingestion speed

Vector search is not optimized for very large datasets

Future Improvements

Add larger quantized LLM (e.g. Mistral 7B)

Implement hybrid search (keyword + vector)

Improve prompt engineering for more accurate answers

## License

MIT License – free to use for personal and educational purposes.