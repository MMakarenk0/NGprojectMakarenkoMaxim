from flask import Flask, render_template
import string
import secrets
import os



app = Flask("Frontend", template_folder='Frontend/Templates', static_folder='Frontend/static')
app.config['STATIC_FOLDER'] = 'static'

images = os.listdir("Frontend/static/images")
for image in images:
    path = os.path.join("Frontend/static/images", image)
    os.remove(path)

def generateToken(length):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token


@app.route('/', methods=["POST", "GET"])
def index():
    token = generateToken(20)

    return render_template('index.html', token=token)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
