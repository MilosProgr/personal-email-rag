import time
from vector_db import retrieve_emails
from llm_wrapper import generate
from config import EMBEDDING_MODEL, TOP_K
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer(EMBEDDING_MODEL)

def run_query(user_query, user_id, top_k=TOP_K):
    # 1️⃣ Embedding
    start = time.time()
    query_embedding = embed_model.encode(user_query).tolist()
    embedding_time = time.time() - start

    # 2️⃣ Retrieval
    start = time.time()
    emails = retrieve_emails(query_embedding, user_id, top_k=top_k)
    retrieval_time = time.time() - start

    if not emails:
        return f"No emails found for user {user_id} or no relevant content.", embedding_time, retrieval_time, 0

    # 3️⃣ Build prompt
    email_texts = "\n\n".join([f" Email ID: {e[0]}], From: {e[1]}, Subject: {e[2]}, Body: {e[3]}" for e in emails])
    prompt = f"Use the following emails/files to answer the question:\n{email_texts}\n\nQuestion: {user_query}\nAnswer:"

    # 4️⃣ LLM generation
    start = time.time()
    answer = generate(prompt)
    llm_time = time.time() - start

    print(f"Embedding: {embedding_time:.2f}s | Retrieval: {retrieval_time:.2f}s | LLM: {llm_time:.2f}s")
    return answer, embedding_time, retrieval_time, llm_time