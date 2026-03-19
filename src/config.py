# src/config.py
DB_CONFIG = {
    "host": "localhost",
    "port": 5440,
    "dbname": "emails",
    "user": "postgres",
    "password": "yourpassword"
}

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # za embeddings
# Za test LLM, manji model da ne troši puno RAM-a
LLM_MODEL_PATH = "bigscience/bloom-560m"  
TOP_K = 5  # koliko emaila vratiti za query