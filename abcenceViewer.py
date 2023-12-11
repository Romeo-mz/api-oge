from flask import Flask, render_template
from api import API
from dataProcessing import format_absence_data, absences_by_course
import json

app = Flask(__name__, template_folder='front/html', static_folder='front/js')

@app.route('/')
def home():
    api = API()
    api.login()
    absences = api.getAllAbsences()
    formatted_absences = format_absence_data(absences)
    absences_course_json = absences_by_course(formatted_absences)
    
    # Parse the JSON back to a Python object
    absences_course = json.loads(absences_course_json)

    labels = [absence['course'] for absence in absences_course]
    values = [absence['total'] for absence in absences_course]

    data = {
        'labels': labels,
        'values': values
    }
    return render_template('graph.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
