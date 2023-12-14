from flask import Flask, render_template, redirect, url_for, session, request
from api import API
from dataProcessing import format_absence_data, absences_by_course
import json
import requests

app = Flask(__name__, template_folder='front', static_folder='front/static')
app.secret_key = 'your_secret_key_here'
api = API()

def get_absences_data():
    absences = api.getAllAbsences()
    formatted_absences = format_absence_data(absences)
    absences_course_json = absences_by_course(formatted_absences)
    return json.loads(absences_course_json)

@app.route('/')
def home():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    absences_course = get_absences_data()

    labels = [absence['course'] for absence in absences_course]
    values = [absence['total'] for absence in absences_course]

    data = {
        'labels': labels,
        'values': values
    }
    return render_template('static/html/graph.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logic to check login credentials
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials here using the API login
        if api.check_login(username, password):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            # Handle incorrect credentials
            return render_template('static/html/login.html', error=True)

    return render_template('static/html/login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
