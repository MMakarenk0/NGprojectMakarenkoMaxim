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

    file.save(f'../Frontend/static/images/{token}.png')

    return redirect('/', 302)

@app.route('/invertImage', methods=['POST'])
def invertImage():
    startTime = time.time()
    token = request.form.get('token')
    filePath = f"../Frontend/static/images/{token}.png"
    img = Image.open(filePath).convert('RGBA')
    threadManager(threadNumber=4, func=invertColors, args=(img, filePath))
    print(time.time()-startTime)
    return f"/static/images/{token}.png"

tokens = {}    
    
@app.route('/extendLifeTime', methods=['POST'])
def extendTime():
    token = request.form.get('token')
    currentTime = datetime.now()
    tokens[token] = datetime.now() + timedelta(minutes=10)

    keysToRemove = []

    for key in tokens.keys():
        if tokens[key] <= currentTime:
            if os.path.exists(f'../Frontend/static/images/{key}.png'):
                os.remove(f'../Frontend/static/images/{key}.png')
                keysToRemove.append(key)
            else:
                keysToRemove.append(key) 

    for key in keysToRemove:
        tokens.pop(key)    

    return 'Time extended'            

app.run(host="0.0.0.0", port=8083, debug=True)