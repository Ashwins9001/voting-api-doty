# models.py
from pydantic import BaseModel
from typing import List, Optional

# Model for a User
class User(BaseModel):
    id: int
    name: str

# Model for a Question
class Question(BaseModel):
    id: int
    question_text: str
    choices: List[int]  # List of user IDs as answer choices (users as choices)

# Model for a Vote
class Vote(BaseModel):
    user_id: int
    question_id: int
    answer_user_id: int  # The user being voted for

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "question_id": self.question_id,
            "answer_user_id": self.answer_user_id
        }

# Model for the response showing the vote count for each user as an answer choice
class VoteResults(BaseModel):
    user_name: str
    vote_count: int
