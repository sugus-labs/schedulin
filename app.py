
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello from Flask!'

@app.route('/bye')
def bye_bye():
    return 'Bye bye from Flask!'

