from flask import Flask, request
from flask_cors import CORS
from tika import parser
from parser import ParseHH
from time import sleep

import json
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'index'


def predict(vacancy_text):
    return vacancy_text


@app.route('/predict_text', methods=['GET', 'POST'])
def predict_text():
    content_type = request.headers.get('Content-Type')

    text = str(request.json['vacancy'])
    if content_type == 'application/json':
        if 'vacancy/' in text:
            return predict_url(request)
        else:
            prediction = predict(text)
            return prediction


@app.route('/predict_pdf', methods=['POST'])
def predict_pdf():
    file = request.files['file']
    file.save(file.filename)

    if file:
        parsed = parser.from_file(file.filename)
        prediction = predict(parsed['content'].strip())
        os.remove(file.filename)
        return prediction
    else:
        return "{'error': 'File not found'}"


# @app.route('/predict_url', methods=['POST'])
def predict_url(req):
    url = req.json['vacancy']
    parser_hh = ParseHH(url)

    print(parser_hh.title())
    print(parser_hh.description())
    prediction = predict(parser_hh.description())
    return prediction


@app.errorhandler(404)
def page_not_found(e):
    return e.description, 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=26601)