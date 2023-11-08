import os
from flask import Flask, render_template, redirect, request, url_for, session
import requests

app = Flask(__name__)

quiz_data = {
    'name': '',
    'description': '',
    'quiz': []
}

app.jinja_env.globals['quiz_data'] = quiz_data
app.jinja_env.globals['auth'] = None

# Handles resetting the data
def reset():
    quiz_data['name'] = ''
    quiz_data['description'] = ''
    quiz_data['quiz'] = []

    app.jinja_env.globals.update(quiz_data=quiz_data)
    app.jinja_env.globals.update(auth=None)


#################################################################################################
# APP ROUTES
#################################################################################################

# Initial page
@app.route('/', methods=['GET', 'POST'])
def index():
    if app.jinja_env.globals['auth'] == None:
            auth = request.args.get("auth")
            app.jinja_env.globals['auth'] = auth

    if auth == 0:
        return render_template('authError.html')
    else:
        return render_template('index.html')

# Handles form submission from the user and redirects
@app.route('/update', methods=['POST'])
def updateData():
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    if not(len(quiz_data['name']) > 0 and len(quiz_data['description']) > 0):
        quiz_data['name'] = request.form.get('quiztitle')
        quiz_data['description'] = request.form.get('quizdescription')
    
    form_data = {
        'question': request.form.get('question'),
        'correctanswer': request.form.get(request.form['correct']),
        'badanswers': [],
        'answerChoices': [request.form.get('optionA'), request.form.get('optionB'), request.form.get('optionC'), request.form.get('optionD')]
    }

    for answer in form_data['answerChoices']:
        if answer != form_data['correctanswer']:
            form_data['badanswers'].append(answer)

    quiz_data['quiz'].append(form_data)

    app.jinja_env.globals.update(quiz_data=quiz_data)

    return redirect(url_for('index'))
    
# Sends the data to the QuizStore and redirects to the main page
@app.route('/congrats', methods=['GET', 'POST'])
def submitQuiz():
    if request.method == 'POST':
        if 'createQuiz' in request.form:

            for i in range(len(quiz_data['quiz'])):
                quiz_data['quiz'][i].pop('answerChoices')

            url = "http://quarzlet-store:8002/addquiz"
            response = requests.post(url, json=quiz_data)

            reset()
            
            return render_template("congrats.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port)
