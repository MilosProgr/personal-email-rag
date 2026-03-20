from rag_pipeline import run_query
from user_auth import authenticate

queries = [
    ("user1", "What did Alice say about the Q4 budget?"),
    ("user2", "Show me emails discussing API integration"),
    ("user1", "Summarize all conversations about the product launch"),
    ("user2", "When did I last hear from the marketing team?")
]

for user_id, query in queries:
    try:
        authenticate(user_id)
        print(f"\n=== User: {user_id} ===")
        print(f"Query: {query}")
        answer = run_query(query, user_id)
        print("Answer:\n", answer)
    except ValueError as e:
        print(e)