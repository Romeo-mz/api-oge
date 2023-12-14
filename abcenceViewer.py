from flask import Flask, render_template, redirect, url_for, session, request
from api import API
from dataProcessing import format_absence_data, absences_by_course
import json

app = Flask(__name__, template_folder='front', static_folder='front/static')
api = API()

def fetch_absences_data():
    try:
        absences = api.get_all_absences()
        formatted_absences = format_absence_data(absences)
        absences_course_json = absences_by_course(formatted_absences)
        return json.loads(absences_course_json)
    except Exception as e:
        # Handle specific exceptions appropriately
        print(f"Error fetching absences: {e}")
        return []

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    absences_course = fetch_absences_data()
    if not absences_course:
        # Handle absence data fetching failure
        return render_template('error.html', error="Failed to retrieve absence data")

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
        username = request.form.get('username')
        password = request.form.get('password')
        
        if api.check_login(username, password):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('static/html/login.html', error=True)

    return render_template('static/html/login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
