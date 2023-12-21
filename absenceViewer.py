import json
import logging
import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, g

from api import API
from dataProcessing import format_absence_data, absences_by_course

app = Flask(__name__, template_folder='front', static_folder='front/static')
app.secret_key = os.getenv("SECRET_KEY")

@app.before_request
def before_request():
    g.api = None
    if 'username' in session and 'password' in session:
        g.api = API(session['username'], session['password'])
        g.api.login()



def fetch_absences_data():
    if g.api is None:
        return []
    try:
        absences = g.api.get_all_absences()
        formatted_absences = format_absence_data(absences)
        absences_course_json = absences_by_course(formatted_absences)
        return json.loads(absences_course_json)
    except Exception as e:
        # Improved error handling: log exceptions
        logging.error(f"Error fetching absences: {e}")
        return []

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    absences_course = fetch_absences_data()
    if not absences_course:
        logging.error("Error fetching absences")

    labels = [absence['course'] for absence in absences_course]
    values = [absence['total'] for absence in absences_course]

    data = {
        'labels': labels,
        'values': values
    }
    return render_template('static/html/graph.html', data=data)

@app.route('/logout')
def logout():
    print("Logout")
    session.pop('logged_in', None)
    session.pop('username', None)  # Remove stored username from session
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return handle_login()

    return render_template('static/html/login.html')

def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please enter both username and password', 'error')
        return render_template('static/html/login.html')

    g.api = API(username, password)
    if g.api.login():
        session['logged_in'] = True
        session['username'] = username  # Store username in session
        session['password'] = password #is this safe?
        return redirect(url_for('home'))
    else:
        flash('Invalid credentials', 'error')
        return render_template('static/html/login.html')

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.ERROR)
    app.run(debug=True)