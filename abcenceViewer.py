from flask import Flask, render_template
from api import API
from dataProcessing import format_absence_data, absences_by_course
import json
import requests

app = Flask(__name__, template_folder='front', static_folder='front/static')
api = API()
api.login()

@app.route('/')
def home():    
    absences = api.getAllAbsences()
    formatted_absences = format_absence_data(absences)
    absences_course_json = absences_by_course(formatted_absences)
    absences_course = json.loads(absences_course_json)

    labels = [absence['course'] for absence in absences_course]
    values = [absence['total'] for absence in absences_course]

    data = {
        'labels': labels,
        'values': values
    }
    return render_template('static/html/graph.html', data=data)

@app.route('/login')
def login():
    return render_template('static/html/login.html')
   
if __name__ == '__main__':
    app.run(debug=True)
