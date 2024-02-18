import os
import datetime
import pytz
import json

from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, comp, get_system_prompt

# Configure application
app = Flask(__name__)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    """Request quiz topic and save to file"""
    if request.method == "POST":
        if not request.form.get("topic"):
            topic = "any"
        else:
            topic = request.form.get("topic")
        with open("topic.txt", "w") as file:
            file.write(topic)
        return render_template("index.html")
        
    else:
        return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    prompt, topic = get_system_prompt()
    response = comp(prompt, MaxToken=3000, outputs=3)
    quiz = json.loads(response)["quiz"]
    questions = []

    for qst in quiz:
        question = {}
        question["number"] = "Q" + qst["question_number"]
        question["text"] = qst["question"]
        question["answers"] = []
        for answ in qst["answers"]:
            answer = {}
            answer["number"] = "A" + str(qst["answers"].index(answ))
            answer["text"] = answ
            if answ == qst["correct_answer"]:
                answer["correctness"] = "correct"
            else:
                answer["correctness"] = "wrong"
            question["answers"].append(answer)
        questions.append(question)

    return render_template("quiz.html", topic = topic.capitalize(), questions = questions)
