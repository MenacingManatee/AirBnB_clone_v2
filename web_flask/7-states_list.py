#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask, request, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def hello_hbnb():
    from models import storage
    from models.state import State
    states = storage.all(State)
    ret = {state.id: state.name for state in states.values()}
    return render_template("7-states_list.html", states=sorted(ret.items()))

if __name__ == '__main__':
    app.run('0.0.0.0')
