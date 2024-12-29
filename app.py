# app.py
from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Question, Vote, VoteResults

users_db = {
    1: User(id=1, name="Ashwin"),
    2: User(id=2, name="Arjun"),
    3: User(id=3, name="Ahnaf"),
    4: User(id=4, name="Amik"),
    5: User(id=5, name="Mush"),
    6: User(id=5, name="Harshal"),
    7: User(id=5, name="Kandarp"),
    8: User(id=5, name="Ash"),
    9: User(id=5, name="Prabhjot"),
    10: User(id=5, name="Kaustav")
}

questions_db = {
    1: Question(id=1, question_text="Who is the most toxic dog", choices=[1,2,3,4,5,6,7,8,9,10]),
    2: Question(id=2, question_text="Who is the most lightweight dog", choices=[1,2,3,4,5,6,7,8,9,10]),
    3: Question(id=3, question_text="Who is the most dramatic dog", choices=[1,2,3,4,5,6,7,8,9,10])
}

votes_db = {
    1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6:0, 7:0, 8:0, 9:0, 10:0},
    2: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6:0, 7:0, 8:0, 9:0, 10:0},
    3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6:0, 7:0, 8:0, 9:0, 10:0}
}

app = FastAPI()

# Endpoint to create a new user
@app.post("/users/", response_model=User)
async def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return user

# Endpoint to create a new question with users as choices
@app.post("/questions/", response_model=Question)
async def create_question(question: Question):
    if question.id in questions_db:
        raise HTTPException(status_code=400, detail="Question already exists")
    # Check if all choices are valid users
    for user_id in question.choices:
        if user_id not in users_db:
            raise HTTPException(status_code=400, detail=f"User {user_id} not found as a valid choice")
    
    questions_db[question.id] = question
    # Initialize votes for each user choice to 0
    votes_db[question.id] = {user_id: 0 for user_id in question.choices}
    return question

# Endpoint to allow users to vote for another user as the answer to a question
@app.post("/vote/")
async def vote(vote: Vote):
    if vote.user_id not in users_db:
        raise HTTPException(status_code=404, detail="Voter user not found")
    if vote.question_id not in questions_db:
        raise HTTPException(status_code=404, detail="Question not found")
    if vote.answer_user_id not in users_db:
        raise HTTPException(status_code=404, detail="Voted user not found")
    if vote.answer_user_id not in questions_db[vote.question_id].choices:
        raise HTTPException(status_code=400, detail="User not a valid choice for this question")
    
    # Record the vote
    votes_db[vote.question_id][vote.answer_user_id] += 1
    return {"message": f"User {vote.user_id} voted for user {vote.answer_user_id} on question {vote.question_id}"}

# Endpoint to get total votes by person per question
@app.get("/total-votes/{question_id}", response_model=dict)
async def get_total_votes(question_id: int):
    if question_id not in votes_db:
        raise HTTPException(status_code=404, detail="Votes not found for this question")

    # Retrieve the votes for the specific question
    votes_for_question = votes_db[question_id]
    
    # Prepare a list of votes by person (user_id)
    result = []
    for user_id, vote_count in votes_for_question.items():
        user_name = users_db[user_id].name  # Get the user's name from users_db
        result.append({"user_name": user_name, "vote_count": vote_count})
    
    return {
        "question_id": question_id,
        "votes": result  # Return the votes for each user in the question
    }