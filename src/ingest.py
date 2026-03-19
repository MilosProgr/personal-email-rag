# src/ingest.py
import json
from config import DB_CONFIG
from vector_db import insert_email
from sentence_transformers import SentenceTransformer
from attachment_parser import parse_attachment

# Učitaj sample dataset
with open("../data/sample_emails.json") as f:
    emails = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

for email in emails:
    body = email["body"]

    # Parse attachments
    attachment_text = ""
    for file in email.get("attachments", []):
        attachment_text += parse_attachment(file) + "\n"

    # Combine body + attachments
    full_text = body + "\n" + attachment_text

    # Embedding
    embedding = model.encode(full_text).tolist()

    insert_email(email, embedding)