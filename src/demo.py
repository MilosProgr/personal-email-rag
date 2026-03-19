from rag_pipeline import run_query
import time

# List of example queries per user
queries = [
    ("user1", "What did Alice say about the Q4 budget?"),
    ("user2", "Show me emails discussing API integration"),
    ("user1", "Summarize all conversations about the product launch")
]

for user_id, query in queries:
    print(f"\n=== User: {user_id} ===")
    print(f"Query: {query}")

    # Measure total time for retrieval + LLM generation
    start_time = time.time()
    answer = run_query(query, user_id)
    elapsed = time.time() - start_time

    print("Answer:\n", answer)
    print(f"Time elapsed: {elapsed:.2f} seconds")