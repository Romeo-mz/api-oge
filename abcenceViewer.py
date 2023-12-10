from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def home():
    data = {
        "name": "GARNIER LIONEL",
        "hours": [15.30, 17.30],
        "subject": "Maths",
        "date": "19/01/2023"
    }