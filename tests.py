

# dict -> qid: question_obj
questions_db = {}

# list of `User`
users_db = [{'id': i, 'name': j} for i,j in zip(range(5), ['a','b','c','d','e'])]

# dict -> qid: dict[possibility_user_id: num_votes_for_this_selection]
votes_db = {}


# Endpoint to create a new question with users as choices
def create_question(question):
    if question['id'] in questions_db:
        assert False, "Question already exists"
    # Check if all choices are valid users
    for user_id in question['choices']:
        if user_id not in map(lambda x:x['id'],users_db):
            assert False, f"User {user_id} not found as a valid choice"
    
    questions_db[question['id']] = question
    # Initialize votes for each user choice to 0
    votes_db[question['id']] = {user_id: 0 for user_id in question['choices']}
    return question


question_obj = {
    'id' : 0,
    'question_text': 'sample question',
    'choices' : list(range(5))
}

print('init')
print(f'{users_db=}')
print(f'{questions_db=}')
print(f'{votes_db=}')
print()

created_question = create_question(question=question_obj)


print(f'{created_question=}')
print()
print(f'{users_db=}')
print(f'{questions_db=}')
print(f'{votes_db=}')