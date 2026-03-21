import os
import json
from gmail_client import get_gmail_service, get_drive_service, list_messages, get_message, get_attachments, download_drive_files
from attachment_parser import parse_attachment
from vector_db import insert_email
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_PATH = os.path.join(BASE_DIR, "data", "users.json")

with open(USERS_PATH) as f:
    users = json.load(f)

model = SentenceTransformer(EMBEDDING_MODEL)

for user in users:
    user_id = user['user_id']
    # Gmail ingestion
    service = get_gmail_service(user_id)
    emails = []
    for msg_meta in list_messages(service, max_results=10):
        email = get_message(service, msg_meta['id'])
        email['attachments'] = get_attachments(service, msg_meta['id'])
        email['user_id'] = user_id
        emails.append(email)

    for email in emails:
        full_text = email['body'] + "\n"
        for att in email.get('attachments', []):
            full_text += parse_attachment(att) + "\n"
        embedding = model.encode(full_text).tolist()
        insert_email(email, embedding)

    # Optional Drive ingestion
    drive_service = get_drive_service(user_id)
    drive_files = download_drive_files(drive_service, folder_id="1HO7riAgT66kBj71XfheZh8wTSlQCoXet")
    for file in drive_files:
        full_text = parse_attachment(file)
        email_doc = {
            "user_id": user_id,
            "sender": "drive",
            "recipient": "me",
            "subject": file,
            "body": full_text,
            "timestamp": "2026-03-19T00:00:00",
            "attachments": [file]
        }
        embedding = model.encode(full_text).tolist()
        insert_email(email_doc, embedding)