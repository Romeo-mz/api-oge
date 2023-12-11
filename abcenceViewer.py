from flask import Flask, render_template
from api import API
from dataProcessing import format_absence_data
import json

app = Flask(__name__, template_folder='front/html', static_folder='front/js')

@app.route('/')
def home():
    api = API()
    api.login()
    absences = api.getAllAbsences()
    formatted_absences = format_absence_data(absences)
    labels = [absence['course'] for absence in formatted_absences]
    values = [absence['status'] for absence in formatted_absences]

    print(values)
    print(labels)
    data = {
        'labels': labels,
        'values': values
    }
    return render_template('graph.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
