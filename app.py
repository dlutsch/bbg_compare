import json
from flask import (Flask, render_template, redirect,
                   url_for, request, make_response)
from bgg import find_games

app = Flask(__name__)


def get_saved_data():
    try:
        data = json.loads(request.cookies.get('user'))
    except TypeError:
        data = {}
    return data


@app.route('/')
def index():
    data = get_saved_data()
    return render_template('index.html', saves=data)


@app.route('/save', methods=['POST'])
def save():
    response = make_response(redirect(url_for('games')))
    data = get_saved_data()
    data.update(dict(request.form.items()))
    response.set_cookie('user', json.dumps(dict(request.form.items())))
    return response


@app.route('/games')
def games():
    data = get_saved_data()
    user = data['user_name']
    results = find_games(str(user))
    # print(results)
    # import pdb; pdb.set_trace()
    return render_template('game.html', games=results)


app.run(debug=True, host='0.0.0.0')
