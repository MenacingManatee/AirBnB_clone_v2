#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask, request, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(x):
    from models import storage
    storage.close()


@app.route('/states_list')
def states_list():
    '''lists all states as list items'''
    from models import storage
    from models.state import State
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=sorted(
        states, key=lambda x: x.name))


@app.route('/cities_by_states')
def cities_states():
    '''lists all cities by states as list items'''
    from models import storage
    from models.state import State
    states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=sorted(
        states, key=lambda x: x.name))


@app.route('/states')
@app.route('/states/<id>')
def states(id=None):
    '''lists one or many states'''
    from models import storage
    from models.state import State
    states = storage.all(State)
    if id is not None:
        states = states.get("State.{}".format(id))
        return render_template('9-states.html', states=states, cities=True)
    else:
        states = states.values()
        return render_template('9-states.html', states=sorted(
            states, key=lambda x: x.name), cities=False)

if __name__ == '__main__':
    app.run('0.0.0.0')
