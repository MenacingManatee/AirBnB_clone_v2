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


@app.route('/number/<int:n>')
def isInt(n):
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>')
def num_template(n):
    ret = '''<!DOCTYPE html>
<HTML lang="en">
    <HEAD>
        <TITLE>HBNB</TITLE>
    </HEAD>
    <BODY>
        <H1>Number: {}</H1>
    </BODY>
</HTML>
'''.format(n)
    return ret


if __name__ == '__main__':
    app.run('0.0.0.0')
