import requests
import os
from flask import Flask, render_template, request
import requests

import json



import os
import requests

APP_ROOT = ''
api_key = 'acc_17051bbae2be7da'
api_secret = '9ee2994bb16e44b3c38eb4a110aff231'

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    template_name = 'display.html'
    tag_dict = {}
    image_url = None
    target = os.path.join(APP_ROOT, '/static')

    if not os.isdir(target):
        os.mkdir(target)
        
    file = request.files['file']
    filename = file.filename
    
    destination = f'{target}/{filename}'
    file.save(destination)
     
    image_url = f"{request.host_url}static/{filename}"
    response = requests.get(f"https://api.imagga.com/v2/tags?image_url=${image_url}", auth=(api_key, api_secret))
    
    if (response.json()['status']['type'] == 'success'):
        tags = response.json()['result']['tags']
        
        for tag in tags:
            tags[tag['tag']] = tag['confidence']
            
    return render_template(template_name, tag_dict = tag_dict, image_url=image_url)




if __name__ == "__main__":
    app.run(debug="true")


# image_url = 'https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg'


# response = requests.get(
#         'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
#         auth=(api_key, api_secret))

# data= response.json()
# for result in data['result']['tags']:
#     print(result)

# response_json = json.loads(response.text)
# myAPI = response_json.items()
# value_list = [value for key, value in myAPI]
# # tags_list = response_json['result']['tags']
# print(type(value_list))
# print(value_list)