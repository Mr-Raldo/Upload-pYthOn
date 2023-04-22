import requests
import os

from flask import Flask, render_template, request
import urllib.request
import json


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
api_key = 'acc_b39a71a9380336a'
api_secret = 'a6f64ed2a3df99d24dfa1d4eb3ba92ec'





app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    tag_dict = {}
    
    target = os.path.join(APP_ROOT, 'static/')

    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files['file']
    filename = file.filename
    destination = "/".join([target, filename])
    file.save(destination)

    imageURL = request.host_url + 'static/' + filename

    image_url = imageURL

    response = requests.get(
        'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
        auth=(api_key, api_secret))

    
    
   
    
    while (response.json()['status']['type'] == 'error'):
        print(response.json())
        # for tag in tags:
        #     tags['tag'] = tag['confidence']
        #     print(tags)  
            
        if (response.json()['status']['type'] == 'success'):
            print(response.json())
            # tags = response.json()
            # for tag in tags:
            #     tags['tag'] = tag['confidence']
            # print(tags)  
            break
    
        
   
    return render_template('display.html', image_url=image_url)






if __name__ == "__main__":
    app.run(debug="true")



