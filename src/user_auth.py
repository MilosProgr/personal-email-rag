# src/user_auth.py
users = {
    "user1": "Alice",
    "user2": "Bob"
}

def authenticate(user_id):
    if user_id in users:
        return True
    else:
        raise ValueError(f"User {user_id} not found")