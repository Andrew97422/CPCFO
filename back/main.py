from flask import Flask
from flask_cors import CORS
from parser import parse_text

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    # parse_text("https://gb.ru/courses/all")
    return 'Hello World!'


app.run(debug=True)
