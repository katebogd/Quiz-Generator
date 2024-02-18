import json

with open('question.json') as f:
    value = json.loads(f.read())
    print(value['question'])
    print(value['answers'])
    print(value['correct_answer'])