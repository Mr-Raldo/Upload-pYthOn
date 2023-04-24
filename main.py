import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from loguru import logger

load_dotenv()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", status=None)


@app.route("/upload", methods=["POST"])
def upload():
    target =  os.path.join(APP_ROOT, 'static/uploads/')

    if not os.path.isdir(os.path.join(APP_ROOT, 'static/uploads/')):
        os.mkdir(target)

    file = request.files['file']
    filename = file.filename
    destination = "/".join([target, filename])
    file.save(destination)

    image_url = f'{request.host_url}static/uploads/{filename}'

    response = requests.get(f'https://api.imagga.com/v2/tags?image_url={image_url}',auth=(api_key, api_secret))
    response = response.json()
    
    if response['status']['type'] == 'error':
        return render_template('index.html', image_url=None, tags=None, status=response['status']['text'])
    
    else:
        return render_template('display.html', image_url=image_url, tags=response['result']['tags'] )


if __name__ == "__main__":
    app.run(debug="true")
