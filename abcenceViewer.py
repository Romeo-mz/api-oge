import json
import logging
import os

from flask import Flask, render_template, redirect, url_for, session, request, flash

from api import API
from dataProcessing import format_absence_data, absences_by_course

app = Flask(__name__, template_folder='front', static_folder='front/static')
app.secret_key = os.getenv("SECRET_KEY")
api = API()


def fetch_absences_data(api_instance):
    try:
        absences = api_instance.get_all_absences()
        formatted_absences = format_absence_data(absences)
        absences_course_json = absences_by_course(formatted_absences)
        return json.loads(absences_course_json)
    except Exception as e:
        # Improved error handling: log exceptions
        logging.error(f"Error fetching absences: {e}")
        return []


def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please enter both username and password', 'error')
        return render_template('static/html/login.html')

    if api.check_login(username, password):
        session['logged_in'] = True

        return redirect(url_for('home'))
    else:
        flash('Invalid credentials', 'error')
        return render_template('static/html/login.html')


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    absences_course = fetch_absences_data(api)
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
    session.pop('logged_in', None)
    session.pop('api_username', None)  # Remove stored username
    session.pop('api_password', None)  # Remove stored password
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return handle_login()

    return render_template('static/html/login.html')


if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.ERROR)
    app.run(debug=True)
