#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    return 'Hello HBNB'


@app.route('/hbnb')
def hbnb():
    return 'HBNB'


@app.route('/c/<text>')
def display_text(text):
    text = str(text)
    return text.replace('_', ' ')


@app.route('/python')
@app.route('/python/<text>')
def pythonIs(text='is_cool'):
    text = str(text)
    return "Python {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run('0.0.0.0')
