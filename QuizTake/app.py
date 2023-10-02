###################################################################
# Quarzlet Take Flask Server
# Group 3: Devin Patel, Vish Patel, Aidan Lear
# Purpose: To implement a "Take Quiz" service for the Quarzlet application
#
# The service must:
#   - Provide an entry point for the Quarzlet application.
#   - The first page must prompt the user to either take a quiz or redirect to the QuizMake service.
#   - Send a request to the QuizStore service to fetch all quiz names.
#   - Present the user with a list of quiz names to select from as a sidebar item.
#   - Query the user to select a quiz to take.
#   - Send a request to the QuizStore service to fetch the selected quiz.
#   - Present the quiz to the user and allow them to select one of multiple choice answers.
#   - Grade the quiz according to the correct answers
#   - Present the user with their score.
###################################################################

# Imports
from flask import Flask, render_template, redirect, url_for, request
import random

app = Flask(__name__)


def generate_quiz_list():
    # Make database query for all quiz titles
    quiz_titles = ["Pikachu"*20, "Charizard", "Squirtle", "Jigglypuff",
                   "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"]
    quiz_titles += quiz_titles
    quiz_titles += quiz_titles
    quiz_urls = []

    for title in quiz_titles:
        quiz_urls.append({"name": title, "url": url_for("quiz", quiz=title)})
    quizzes_len = len(quiz_urls)
        
    app.jinja_env.globals.update(quizzes=quiz_urls, quizzes_len=quizzes_len, current_quiz="")


@app.route("/")
def index():
    # Quiz list for sidebar
    generate_quiz_list()

    return render_template("index.html")


@app.route("/quiz")
def quiz():
    # HTTP GET the quiz name
    quiz_name = request.args.get("quiz")
    
    # Use the name to fetch the quiz data from the database
    # @TODO Randomize the order of the questions and answers
    quiz_data = [{"question_num": 1, "question": "What is the best pokemon?", "answers": ["Pikachu", "Charizard", "Squirtle", "Jigglypuff"]},
                 {"question_num": 2, "question": "What is 2 + 2?", "answers": ["4", "5", "6", "7"]},
                 {"question_num": 3, "question": "Who invented the telephone?", "answers": ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Albert Einstein"]},
                 {"question_num": 4, "question": "What color does red and blue make?", "answers": ["Purple", "Green", "Orange", "Yellow"]}]
    
    # If it is not there, then redirect to quiz not found page.
    if not quiz_data:
        return quiz_not_found()
    
    # Update current quiz name in session and render webpage
    app.jinja_env.globals.update(current_quiz=quiz_name)
    return render_template("quiz.html", quiz_data=quiz_data)

@app.route("/submit", methods=["POST"])
def check_quiz():
    if request.method != 'POST':
        return render_template("quiz_not_found.html")
    
    # 
        


def quiz_not_found():
    # Update current quiz name in session and render webpage
    app.jinja_env.globals.update(current_quiz="")
    return render_template("quiz_not_found.html")