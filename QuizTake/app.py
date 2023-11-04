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
from flask import Flask, render_template, redirect, url_for, request, session
import random
import configparser

def init_flask_config():
    # Initialize the Flask secret key from the config file and return it
    
    # Check if config file exists
    import os
    if not os.path.exists(r'config/flask.ini'):
        raise Exception("Please create a config/flask.ini file before running the server. See config/flask.ini.example for an example.")
    
    # Read the secret key from the config file
    config = configparser.ConfigParser()
    config.read(r'config/flask.ini')

    if len(config['credentials']['secret']) < 64:
        raise Exception("Please change the secret key to a cryptographically secure token in config/flask.ini before running the server.\n"
                        + "The token must be at least 64 characters. One can be generated in the Python REPL with secrets.token_hex(32).")
    
    return config['credentials']['secret']
    
###################################################################
# Main - Initialize the Flask app
###################################################################
app = Flask(__name__)
app.secret_key = init_flask_config()


# App Functions
def generate_quiz_list():
    # Create quiz list for sidebar
    # @TODO Make database query for all quiz titles
    # @DEBUG - Hardcoded quiz data
    quiz_titles = ["Pikachu"*20, "Charizard", "Squirtle", "Jigglypuff",
                   "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"]
    quiz_titles += quiz_titles
    quiz_titles += quiz_titles
    quiz_urls = []

    # Assign a url for every quiz title
    for title in quiz_titles:
        quiz_urls.append({"name": title, "url": url_for("quiz", quiz=title)})
    quizzes_len = len(quiz_urls)
    
    # Set the user's current quiz to empty
    session['current_quiz'] = ""
    
    # Update the global variables for the quiz list and the current quiz. quizzes_len is used by the Jinja syntax to determine if the quiz list is empty or not.
    app.jinja_env.globals.update(quizzes=quiz_urls, quizzes_len=quizzes_len, current_quiz=session['current_quiz'])


@app.route("/")
def index():
    # Landing page for the app
    
    # Quiz list for sidebar
    generate_quiz_list()

    return render_template("index.html")


@app.route("/quiz")
def quiz():
    # Get the quiz name
    quiz_name = request.args.get("quiz")
    
    # Use the name to fetch the quiz data from the database
    # @TODO Randomize the order of the questions and answers
    # @DEBUG - Hardcoded quiz data
    quiz_data = [{"question_num": 0, "question": "What is the best pokemon?", "answers": ["Pikachu", "Charizard", "Squirtle", "Jigglypuff"], "correct_answer": "Pikachu"},
                 {"question_num": 1, "question": "What is 2 + 2?", "answers": ["4", "5", "6", "7"], "correct_answer": "4"},
                 {"question_num": 2, "question": "Who invented the telephone?", "answers": ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Albert Einstein"], "correct_answer": "Alexander Graham Bell"},
                 {"question_num": 3, "question": "What color does red and blue make?", "answers": ["Purple", "Green", "Orange", "Yellow"], "correct_answer": "Purple"}]
    
    # If it is not there, then redirect to quiz not found page.
    if not quiz_data:
        redirect(url_for("quiz_not_found"))
    
    # Update current quiz name in session and render webpage
    session['quiz_data'] = quiz_data
    session['current_quiz'] = quiz_name
    app.jinja_env.globals.update(current_quiz=session['current_quiz'])
    return render_template("quiz.html", quiz_data=quiz_data)


@app.route("/submit", methods=["POST"])
def check_quiz():
    if request.method != 'POST':
        return render_template("quiz_not_found.html")
    
    user_answers = []
    num_correct = 0
    
    # Fetch quiz data from session
    quiz_data = session['quiz_data']
    
    # Check user answers against correct answers
    for question in quiz_data:
        question_num = question["question_num"]
        user_answer = request.form.get("question{}".format(question_num))
        user_answers.append(user_answer)
        if user_answer == question["correct_answer"]: num_correct += 1
        
    # Pack data for results page
    results = {"user_answers": user_answers, "quiz_data": quiz_data, "num_correct": num_correct, "num_questions": len(quiz_data)}
    
    return render_template("results.html", results=results)
    

@app.route("/quiz_not_found")
def quiz_not_found():
    # Update current quiz name in session and render webpage
    session['current_quiz'] = ""
    app.jinja_env.globals.update(current_quiz=session['current_quiz'])
    return render_template("quiz_not_found.html")

