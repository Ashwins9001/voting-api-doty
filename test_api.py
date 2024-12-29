from fastapi.testclient import TestClient
from app import app, users_db, votes_db, questions_db
from models import User, Vote, Question
import json

client = TestClient(app)

payload = {
        "user_id": 1,           # The ID of the user casting the vote
        "question_id": 2,       # The ID of the question being voted on
        "answer_user_id": 2     # The ID of the user being voted for
    }
client.post("/vote/", json=payload)

response = client.get(f"/total-votes/2")
print(response.json())