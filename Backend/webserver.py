from flask import Flask, make_response, redirect, request
from datetime import datetime, timedelta
import shutil
from imageWorker import *
from flask_cors import CORS
import os
import time


app = Flask("Ajax_server")

CORS(app)

undoHistory = {}
redoHistory = {}
tokens = {}    
usersShifts = {}   

@app.route('/')
def index():
    return "home page"

@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    token = request.form.get('token')
    file = request.files['file']
    createActionHistory(token, undoHistory, redoHistory)

    if file.filename == '':
        return 'No selected file', 400

    file.save(f'../Frontend/static/images/{token}.bmp')
    filePath = f"../Frontend/static/images/{token}.bmp"
    img = Image.open(filePath).convert('RGB')
    updateHistory(token, undoHistory, redoHistory, img.copy())


    return redirect('/', 302)

@app.route('/invertImage', methods=['POST'])
def invertImage():
    # startTime = time.time()
    token = request.form.get('token')
    createActionHistory(token, undoHistory, redoHistory)

    filePath = f"../Frontend/static/images/{token}.bmp"
    img = Image.open(filePath).convert('RGB')
    imageParts, width, height = cropImage(img)
    threadManager(threadNumber=4, func=invertColors, args=(imageParts,))
    mergedImage = mergeImage(filePath, imageParts, width, height)
    updateHistory(token, undoHistory, redoHistory, mergedImage.copy())
    # print(time.time()-startTime)

    return f"/static/images/{token}.bmp" 
    
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

    createActionHistory(token, undoHistory, redoHistory)
    
    
    # startTime = time.time()

    filePath = f"../Frontend/static/images/{token}.bmp"
    previewPath = f"../Frontend/static/preview_images/{token}.bmp"
    img = Image.open(filePath).convert('RGB')
    imageParts, width, height = cropImage(img)
    threadManager(threadNumber=4, func=imageColorShift, args=(imageParts, usersShifts[token],))
    mergedImage = mergeImage(previewPath, imageParts, width, height)
    updateHistory(token, undoHistory, redoHistory, mergedImage.copy())
    # print(time.time()-startTime)

    return f"/static/preview_images/{token}.bmp"

@app.route('/submitOffset', methods=['POST'])
def sumbitOffset():
    token = request.form.get('token')
    if os.path.exists(f'../Frontend/static/images/{token}.bmp'):
        os.remove(f'../Frontend/static/images/{token}.bmp')
        shutil.move(f"../Frontend/static/preview_images/{token}.bmp", "../Frontend/static/images/")
        return f'/static/images/{token}.bmp'
    else:
        return "File not found"

@app.route('/undo', methods=['POST'])
def undo():
    token = request.form.get('token')
    filePath = f"../Frontend/static/images/{token}.bmp"
    
    if token in undoHistory and len(undoHistory[token]) >= 2:
        previous_image = undoHistory[token][-2].copy()
        
        previous_image.save(filePath)
        
        redoHistory[token].append(undoHistory[token].pop())
        
    return f"/static/images/{token}.bmp"

@app.route('/redo', methods=['POST'])
def redo():
    token = request.form.get('token')
    filePath = f"../Frontend/static/images/{token}.bmp"
    
    if token in redoHistory and len(redoHistory[token]) >= 1:
        next_image = redoHistory[token].pop()

        next_image.save(filePath)
        
        undoHistory[token].append(next_image.copy())
        
    return f"/static/images/{token}.bmp"
    
app.run(host="0.0.0.0", port=8083, debug=True)