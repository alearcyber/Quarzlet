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
import requests


def init_flask_config():
    # Initialize the Flask secret key from the config file and return it

    # Check if config file exists
    import os
    if not os.path.exists(r'config/flask.ini'):
        raise Exception(
            "Please create a config/flask.ini file before running the server. See config/flask.ini.example for an example.")

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
    response = requests.get("http://quarzlet-store:8002/available")
    data = response.json()['quizzes']

    # Gather all the quiz titles
    quiz_titles = []
    for quiz in data:
        quiz_titles.append(quiz['name'])

    # Assign a url for every quiz title
    quiz_urls = []
    for title in quiz_titles:
        quiz_urls.append({"name": title, "url": url_for("quiz", quiz=title)})
    quizzes_len = len(quiz_urls)

    # Set the user's current quiz to empty
    session['current_quiz'] = ""

    # Update the global variables for the quiz list and the current quiz. quizzes_len is used by the Jinja syntax to determine if the quiz list is empty or not.
    app.jinja_env.globals.update(
        quizzes=quiz_urls, quizzes_len=quizzes_len, current_quiz=session['current_quiz'])


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
    url = "http://quarzlet-store:8002/getquiz"
    payload = {"name": quiz_name}
    response = requests.get(url=url, json=payload)

    # Check if the response was successful, if not, send to quiz_not_found page
    if response.status_code != 200:
        redirect(url_for("quiz_not_found"))

    # Get the quiz data from the response
    try:
        data = response.json()['quiz']
    except:
        redirect(url_for("quiz_not_found"))

    # Collect quiz data into format for html pages
    quiz_data = []
    for i, question in enumerate(data, start=0):
        # Randomize order of answers
        answers = [question['correctanswer']] + question['badanswers']
        random.shuffle(answers)
        quiz_data.append({'question_num': i,
                          'question': question['question'],
                          'correct_answer': question['correctanswer'],
                          'answers': answers})

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
        if user_answer == question["correct_answer"]:
            num_correct += 1

    # Pack data for results page
    results = {"user_answers": user_answers, "quiz_data": quiz_data,
               "num_correct": num_correct, "num_questions": len(quiz_data)}

    return render_template("results.html", results=results)


@app.route("/quiz_not_found")
def quiz_not_found():
    # Update current quiz name in session and render webpage
    session['current_quiz'] = ""
    app.jinja_env.globals.update(current_quiz=session['current_quiz'])
    return render_template("quiz_not_found.html")
