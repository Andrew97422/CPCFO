from flask import Flask, request
from flask_cors import CORS
from tika import parser
from parser import ParseHH
from PIL import Image
import os

from recommender import reccomend

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'index'


def predict(id, title, description):
    rec_titles, img = reccomend(id, title, description)
    return rec_titles


@app.route('/predict_text', methods=['GET', 'POST'])
def predict_text():
    content_type = request.headers.get('Content-Type')

    text = str(request.json['vacancy'])
    if content_type == 'application/json':
        if 'vacancy/' in text:
            return predict_url(request)
        else:
            prediction = predict('','',text)
            return prediction


@app.route('/predict_pdf', methods=['POST'])
def predict_pdf():
    file = request.files['file']
    file.save(file.filename)

    if file:
        parsed = parser.from_file(file.filename)
        prediction = predict('','',parsed['content'].strip())
        os.remove(file.filename)
        return prediction
    else:
        return "{'error': 'File not found'}"


# @app.route('/predict_url', methods=['POST'])
def predict_url(req):
    try:
        parser_hh = ParseHH(req.json['vacancy'])
    except:
        return "{'error': 'Vacancy cannot be downloaded from provided URL.((('}"
    prediction = predict(parser_hh.id, parser_hh.title(), parser_hh.description())
    return prediction


@app.errorhandler(404)
def page_not_found(e):
    return e.description, 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=26601)