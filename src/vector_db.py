# src/vector_db.py
import psycopg2
from config import DB_CONFIG, TOP_K

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def insert_email(email, embedding):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO emails (user_id, sender, recipient, subject, body, timestamp, embedding)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (email['user_id'], email['sender'], email['recipient'], email['subject'],
          email['body'], email['timestamp'], embedding))
    conn.commit()
    cur.close()
    conn.close()

def retrieve_emails(query_embedding, user_id, top_k=TOP_K):
    conn = get_connection()
    cur = conn.cursor()

    vector_str = "[" + ",".join(map(str, query_embedding)) + "]"

    sql = f"""
        SELECT id, sender, recipient, subject, body
        FROM emails
        WHERE user_id = %s
        ORDER BY embedding <-> '{vector_str}'::vector
        LIMIT %s;
    """
    cur.execute(sql, (user_id, top_k))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results