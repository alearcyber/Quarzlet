
from flask import Flask, render_template, redirect, request, url_for, session

app = Flask(__name__)
app.secret_key = 'myKey'

quiz_data = {
    'quiz_name': '',
    'questions': []
}

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        quiz_data['quiz_name'] = request.form.get('quiztitle')
        form_data = {
            'question':request.form.get('question'),
            'optionA':request.form.get('optionA'),
            'optionB':request.form.get('optionB'),
            'optionC':request.form.get('optionC'),
            'optionD':request.form.get('optionD'),
            'answer':request.form.get(request.form['correct'])
        }
            
        quiz_data['questions'].append(form_data)

    return render_template("index.html", quiz_data=quiz_data)   

@app.route('/congrats', methods=['GET', 'POST'])
def submitQuiz():
    if request.method == 'POST':
        if 'createQuiz' in request.form:
            session.clear()
            return render_template("congrats.html")    

if __name__ == '__main__':
    app.run(debug=True)