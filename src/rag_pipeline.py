# src/rag_pipeline.py
from vector_db import retrieve_emails
from llm_wrapper import generate
from config import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer(EMBEDDING_MODEL)

def run_query(user_query, user_id):
    # 1️⃣ Embedding query
    query_embedding = embed_model.encode(user_query).tolist()

    # 2️⃣ Retrieve relevant emails
    emails = retrieve_emails(query_embedding, user_id)

    if not emails:
        return f"No emails found for user {user_id} or no relevant content."

    # 3️⃣ Build prompt
    email_texts = "\n\n".join([f"From: {e[1]}, Subject: {e[2]}, Body: {e[3]}" for e in emails])
    prompt = f"Use the following emails to answer the question:\n{email_texts}\n\nQuestion: {user_query}\nAnswer:"

    # 4️⃣ Generate answer using local LLM
    answer = generate(prompt)
    return answer