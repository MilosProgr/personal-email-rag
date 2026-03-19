# personal-email-rag
"Local RAG system for personal emails: ingests Gmail messages, stores embeddings in a vector DB (PGVector), and enables natural language queries using a local LLM. Supports multi-user isolation and contextual answers with attachment indexing."



# Personal Email RAG System

## Overview
This project implements a **local Retrieval-Augmented Generation (RAG) system** for personal emails.  
The system ingests emails, stores them in a vector database, and allows querying using a local LLM.  

---

## Features
- Email ingestion from JSON (simulated Gmail data)
- Vectorization of email text using **sentence-transformers**
- Storage in **PostgreSQL + pgvector**
- Retrieval of relevant emails based on natural language queries
- Local LLM for answer generation
- Multi-user support: each user can only access their own emails

---

## Requirements
- Python 3.11+
- PostgreSQL with `pgvector` extension
- Python packages (see `requirements.txt`):
    transformers
    torch
    sentence-transformers
    psycopg2-binary
    langchain


---

## Setup Instructions
1. Clone the repository:
 ```bash
 git clone <repo_url>
 cd personal-email-rag
 ```
2. Create virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

3. Setup PostgreSQL database:

Create database emails

Enable pgvector extension

Create table:

CREATE TABLE emails (
  id SERIAL PRIMARY KEY,
  user_id TEXT,
  sender TEXT,
  recipient TEXT,
  subject TEXT,
  body TEXT,
  timestamp TIMESTAMP,
  embedding VECTOR(384)
);
4. Update src/config.py with your database credentials and model path.

5. Add your sample email dataset in data/sample_emails.json.

Usage

Run the demo script to test ingestion, retrieval, and answer generation:

python src/demo.py


Example Queries

"What did Alice say about the Q4 budget?"

"Show me emails discussing the API integration project."

"When did I last hear from the marketing team?"

"Summarize all conversations about the product launch."