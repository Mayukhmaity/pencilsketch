from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
import cv2
from PIL import Image
import io
from base64 import b64decode, b64encode

import requests

# Initializing flask app
app = Flask(__name__)
# Adding cors to flask
CORS(app)


# Test API
@app.route("/demo", methods=['GET'])
def get_demo():
    return "This is a demo api"

# Controller-2
@app.route("/from_b64", methods=['POST'])
def from_b64():
    base64string =request.json['base64String']
    base64data = base64string.split(',')
    print(base64data)
    img_data = b64decode(base64data[0])
    image_np = np.fromstring(img_data,dtype=np.uint8)
    img = cv2.imdecode(image_np, flags=cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(img)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(img, invertedblur, scale=270.0)
    img = Image.fromarray(sketch.astype('uint8'))
    rawBytes = io.BytesIO()
    img.save(rawBytes,'JPEG')
    rawBytes.seek(0)
    img_base64 = b64encode(rawBytes.read())
    #print(str(img_base64))
    #base64String = 'data:image/jpeg;base64',+ str(img_base64,encoding='utf-8').split('\'')[0]
    return jsonify({'response':str(img_base64)})