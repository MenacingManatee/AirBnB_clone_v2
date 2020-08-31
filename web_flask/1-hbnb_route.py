#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask


app = Flask(__name___)


@app.route('/')
def hello_hbnb():
    return 'Hello HBNB'


@app.route('/hbnb')
def hbnb():
    return 'HBNB'

if __name__ == '__main__':
    app.run('0.0.0.0')
