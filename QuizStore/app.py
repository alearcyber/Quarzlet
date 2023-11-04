from flask import Flask, jsonify, request
import testdata
import sqlite3
import json
import os

app = Flask(__name__, root_path='./QuizStore/')
DB_PATH = "db"


@app.route('/')
def testpage():
    # out = available_quizzes()
    # return jsonify(out)
    return "hello"

################################################################################################
# ROUTES
################################################################################################

################################################
# for retrieving a quiz from the quiz storage
# errors:
#    460, poorly formatted request
#    461, Can't find existing quiz of that name
################################################


@app.route('/getquiz', methods=['GET'])
def getquiz():
    # parse the incoming JSON
    content: dict = request.json

    # check request formatting
    if "name" not in content.keys():
        return "ERROR: PoorlyFormattedRequest - Expected json with key \"name\" in your request.", 460

    # See if the quiz even exists
    if not does_quiz_exist(content["name"]):
        return f"ERROR: QuizNotFound - Could not find a quiz with the name: {content['name']}", 461

    # get the quiz
    quiz = get_quiz(content["name"])
    return jsonify(quiz)


# Inserts a new quiz to the database
@app.route('/addquiz', methods=['POST'])
def addquiz():
    # parse the incoming JSON
    try:
        content: dict = request.json
    except:
        return "ERROR: JSONParseError - The JSON could not be found, or it could not be parsed as JSON", 462

    # check to see if expected keys are present
    keys = content.keys()
    if "name" not in keys:
        return f"ERROR: PoorlyFormattedRequest - \"name\" key cannot be found.", 460
    if "description" not in keys:
        return f"ERROR: PoorlyFormattedRequest - \"description\" key cannot be found.", 460
    if "quiz" not in keys:
        return f"ERROR: PoorlyFormattedRequest - \"quiz\" key cannot be found.", 460

    # now attempts to parse the rest of the information from the quiz
    try:
        question_list = content['quiz']
        for q in question_list:
            valid = ("question" in q.keys()) and (
                "correctanswer" in q.keys()) and ("badanswers" in q.keys())
            if not valid:
                return f"ERROR: PoorlyFormattedRequest - One of the questions is missing a key in the quiz.", 460
    except:
        return f"ERROR: PoorlyFormattedRequest - There is an unknown issue with the formatting of the sent quiz.", 460

    # add the quiz
    try:
        add_new_quiz(content)
    except:
        jsonify(
            {"status": 0, "Message": "There was an issue adding the quiz to the database. It was NOT added"})

    return jsonify({"status": 1, "Message": "Quiz Was Successfully Added"})


# retrieves the available quizzes and sends them back to the client.
# Expects a GET request with no body.
# TODO - IMPLEMENT THIS
@app.route('/available', methods=['GET'])
def available():
    return jsonify(available_quizzes())


################################################################################################
# Helper Routines
################################################################################################

# checks to see if the quiz name exists in the database
def does_quiz_exist(name):
    results = query(f"""SELECT * FROM quiz where name=?""", (name,))
    return len(results) > 0


# grab the quiz from the database with the given name
# Returns it as a python dictionary
def get_quiz(name):
    # grab quiz
    q = """
    SELECT
        quiz.name, quiz.description, question.question_text, question.right_answer, wrong.answer_text
    FROM
        quiz JOIN question JOIN wrong
    ON
        quiz.name=question.quiz_name AND wrong.question_text = question.question_text
    WHERE
        quiz.name=?
    """

    results = query(q, (name,))

    # parse info describing the quiz
    name = results[0][0]  # name of the quiz
    description = results[0][1]  # description of quiz
    correct_answers = dict()
    incorrect_answers = dict()
    for _, _, question, correctanswer, badanswer in results:
        correct_answers[question] = correctanswer
        if question not in incorrect_answers.keys():
            incorrect_answers[question] = []
        incorrect_answers[question].append(badanswer)

    # create list of questions
    questions = []
    for _, _, question, _, _ in results:
        q = dict()  # dictionary to represent a question in the list of questions
        q["question"] = question
        q["correctanswer"] = correct_answers[question]
        q["badanswers"] = incorrect_answers[question]
        questions.append(q)

    # construct final dictionary of the output
    quiz = dict()
    quiz['name'] = name
    quiz['description'] = description
    quiz['quiz'] = questions
    return quiz


# adds a new quiz to the database
# data should be json properly formatted according to [INSERT WHERE IT IS RECORDEDE HERE]
def add_new_quiz(data):
    # grab info
    name = data['name']
    description = data['description']
    questions = data['quiz']

    # insert into quiz table first
    query(f"""INSERT INTO quiz VALUES (?, ?)""", (name, description))

    # Add all the questions
    for question in questions:
        # data
        q = question['question']
        a = question['correctanswer']
        wrong_answers = question['badanswers']

        # insert into database
        query(f"""INSERT INTO question (question_text, right_answer, quiz_name) VALUES (?, ?, ?)""", (q, a, name))

        # add bad answers
        for wrong_answer in wrong_answers:
            query(
                f"""INSERT INTO wrong (question_text, answer_text) VALUES (?, ?)""", (q, wrong_answer))


##########################################################################################
# What quizzes are available from the database
##########################################################################################
def available_quizzes():
    q = """
    SELECT
        name, description
    FROM
        quiz
    """
    results = query(q, None)
    quizzes = []
    for name, description in results:
        quizzes.append({'name': name, 'description': description})
    return {'quizzes': quizzes}


##########################################################################################
# sends any query to the database
##########################################################################################
def query(q, args):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    if args is None:
        result = cursor.execute(q).fetchall()
    else:
        result = cursor.execute(q, args).fetchall()
    connection.commit()
    connection.close()
    return result


##########################################################################################
# Entry point for the program
##########################################################################################
def main():
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
