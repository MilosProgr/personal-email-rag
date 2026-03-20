import os
import pickle
import io
import base64
from datetime import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

from config import GMAIL_SCOPES, DRIVE_SCOPES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ATTACHMENTS_DIR = os.path.join(DATA_DIR, "attachments")
DRIVE_DIR = os.path.join(DATA_DIR, "drive_files")
CREDENTIALS_PATH = os.path.join(DATA_DIR, "credentials.json")


def get_gmail_service(user_id):
    creds = None
    token_path = os.path.join(DATA_DIR, f"token_{user_id}.pkl")

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError("credentials.json not found in data/ folder")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def get_drive_service(user_id):
    creds = None
    token_path = os.path.join(DATA_DIR, f"token_drive_{user_id}.pkl")

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if not os.path.exists(CREDENTIALS_PATH):
            raise FileNotFoundError("credentials.json not found in data/ folder")
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH, DRIVE_SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)


def list_messages(service, user_id="me", max_results=10):
    results = service.users().messages().list(
        userId=user_id, maxResults=max_results
    ).execute()
    return results.get("messages", [])


def get_message(service, msg_id, user_id="me"):
    msg = service.users().messages().get(
        userId=user_id, id=msg_id, format="full"
    ).execute()

    payload = msg["payload"]
    headers = payload.get("headers", [])

    timestamp_ms = int(msg["internalDate"])
    timestamp = datetime.fromtimestamp(timestamp_ms / 1000)

    email_data = {
        "sender": next((h["value"] for h in headers if h["name"] == "From"), ""),
        "recipient": next((h["value"] for h in headers if h["name"] == "To"), ""),
        "subject": next((h["value"] for h in headers if h["name"] == "Subject"), ""),
        "timestamp": timestamp,
        "body": "",
    }

    def extract_body(parts):
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            elif "parts" in part:
                result = extract_body(part["parts"])
                if result:
                    return result
        return ""

    if "parts" in payload:
        email_data["body"] = extract_body(payload["parts"])
    else:
        data = payload["body"].get("data")
        if data:
            email_data["body"] = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return email_data


def get_attachments(service, msg_id, save_dir=ATTACHMENTS_DIR):
    os.makedirs(save_dir, exist_ok=True)
    msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    attachments = []
    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            filename = part.get("filename")
            if filename:
                att_id = part["body"].get("attachmentId")
                if att_id:
                    att = service.users().messages().attachments().get(
                        userId="me", messageId=msg_id, id=att_id
                    ).execute()
                    data = base64.urlsafe_b64decode(att["data"])
                    file_path = os.path.join(save_dir, filename)
                    with open(file_path, "wb") as f:
                        f.write(data)
                    attachments.append(filename)
    return attachments


def download_drive_files(service, folder_id, save_dir=DRIVE_DIR):
    os.makedirs(save_dir, exist_ok=True)
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id,name)").execute()
    files = results.get("files", [])
    downloaded = []

    for f in files:
        file_id, name = f["id"], f["name"]
        request = service.files().get_media(fileId=file_id)
        file_path = os.path.join(save_dir, name)
        fh = io.FileIO(file_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        downloaded.append(name)
    return downloaded