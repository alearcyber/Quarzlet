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
#   - Present the user with their score
#   - Allow the user to reset the quiz to take it again.
#   - The state of the quiz (i.e., the selected answers or graded quiz) should be saved even if the user clicks to a different quiz.
#     - The state of the quiz can get reset if the user refreshes the page or leaves the site.
###################################################################

# Imports
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


def generate_quiz_list():
    # Make database query for all quiz titles
    quiz_titles = ["Pikachu"*10, "Charizard", "Squirtle", "Jigglypuff",
                   "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"]
    quiz_urls = []

    for title in quiz_titles:
        quiz_urls.append({"name": title, "url": url_for("quiz", quiz=title)})

    app.jinja_env.globals.update(quizzes=quiz_urls, current_quiz="")


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
    # If it is not there, then redirect to quiz not found page.
    quiz_data = {}
    
    return quiz_not_found()
    
    
    # Update current quiz name in session and render webpage
    app.jinja_env.globals.update(current_quiz=quiz_name)
    return render_template("quiz.html", quiz_data=quiz_data)


def quiz_not_found():
    app.jinja_env.globals.update(current_quiz="")
    return render_template("quiz_not_found.html")