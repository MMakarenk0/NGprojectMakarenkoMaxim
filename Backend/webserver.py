from flask import Flask, make_response, redirect, request
from datetime import datetime, timedelta
from imageWorker import *
from flask_cors import CORS
import os
import time

app = Flask("Ajax_server")

CORS(app)

@app.route('/')
def index():
    return "home page"

@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    token = request.form.get('token')
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    file.save(f'../Frontend/static/images/{token}.bmp')

    return redirect('/', 302)

@app.route('/invertImage', methods=['POST'])
def invertImage():
    # startTime = time.time()
    token = request.form.get('token')
    filePath = f"../Frontend/static/images/{token}.bmp"
    img = Image.open(filePath).convert('RGB')
    imageParts, width, height = cropImage(img)
    threadManager(threadNumber=4, func=invertColors, args=(imageParts,))
    mergeImage(filePath, imageParts, width, height)
    # print(time.time()-startTime)

    return f"/static/images/{token}.bmp"

tokens = {}    
    
@app.route('/extendLifeTime', methods=['POST'])
def extendTime():
    token = request.form.get('token')
    currentTime = datetime.now()
    tokens[token] = datetime.now() + timedelta(minutes=5)

    keysToRemove = []

    for key in tokens.keys():
        if tokens[key] <= currentTime:
            if os.path.exists(f'../Frontend/static/images/{key}.bmp'):
                os.remove(f'../Frontend/static/images/{key}.bmp')
                keysToRemove.append(key)
            else:
                keysToRemove.append(key) 

    for key in keysToRemove:
        tokens.pop(key)    

    return 'Time extended'  

usersShifts = {}   

@app.route('/colorshift', methods=['POST'])
def colorshift():
    token = request.form.get('token')   
    if token not in usersShifts.keys():   
        usersShifts[token] = [0, 0, 0]
    value_R = request.form.get('value_R')   
    if value_R:
        usersShifts[token][0] = int(value_R)
    value_G = request.form.get('value_G')   
    if value_G:
        usersShifts[token][1] = int(value_G)
    value_B = request.form.get('value_B')
    if value_B:
        usersShifts[token][2] = int(value_B)
    
    # startTime = time.time()

    filePath = f"../Frontend/static/images/{token}.bmp"
    previewPath = f"../Frontend/static/preview_images/{token}.bmp"
    img = Image.open(filePath).convert('RGB')
    imageParts, width, height = cropImage(img)
    threadManager(threadNumber=4, func=imageColorShift, args=(imageParts, usersShifts[token],))
    mergeImage(previewPath, imageParts, width, height)

    # print(time.time()-startTime)

    return f"/static/images/{token}.bmp"

app.run(host="0.0.0.0", port=8083, debug=True)