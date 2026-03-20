DB_CONFIG = {
    "host": "localhost",
    "port": 5440,
    "dbname": "emails",
    "user": "postgres",
    "password": "yourpassword"
}

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_PATH = "bigscience/bloom-560m"
TOP_K = 5

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.readonly']