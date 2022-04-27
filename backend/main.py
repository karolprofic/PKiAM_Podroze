import hashlib
import json
from flask import Flask, request, jsonify, session
from db_connect import database_connect
from destinations import getTravelDestinations, getFavoritesDestinations
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pkiam-podroze'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)

# pip install -U flask-cors
# set FLASK_APP=main
# flask run

@app.route('/login/', methods=['POST'])
def login():
    params = request.json
    if params['username'] and params['password']:
        db = database_connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '" + params["username"] + "'")
        row = cursor.fetchone()
        password = row[7]
        hashed_password = hashlib.sha256(params["password"].encode('utf-8')).hexdigest()

        if len(row) > 0 and password == hashed_password:
            session['username'] = params["username"]
            return jsonify({'status': 'logged successfully'})
        else:
            return jsonify({'status': 'wrong password'})
    else:
        return jsonify({'status': 'wrong login and password'})


@app.route('/logout/')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'status': 'successfully logged out'})


@app.route("/favorites/", methods=['GET', 'DEL', 'PUT'])
def favorites():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})

    db = database_connect()
    cursor = db.cursor()

    if request.method == 'GET':
        params = request.json
        if not ("user_id" in params):
            return jsonify({"status": "not enough data"})

        cursor.execute("SELECT * FROM favorites WHERE user_id = " + params["user_id"])
        results = cursor.fetchall()
        listOfCites = []
        for i in results:
            listOfCites.append(i[2])
        data = getFavoritesDestinations(listOfCites)
        return jsonify(data)

    if request.method == 'DEL':
        params = request.json
        if not ("user_id" in params and "city" in params):
            return jsonify({"status": "not enough data"})

        sql = "DELETE FROM favorites WHERE user_id = %s AND city = %s"
        val = (params["user_id"], params["city"])
        cursor.execute(sql, val)
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"status": "failure"})
        else:
            return jsonify({"status": "success"})

    if request.method == 'PUT':
        params = request.json
        if not ("user_id" in params and "city" in params):
            return jsonify({"status": "not enough data"})

        sql = "INSERT INTO favorites (user_id, city) VALUES (%s, %s)"
        val = (params["user_id"], params["city"])
        cursor.execute(sql, val)
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"status": "failure"})
        else:
            return jsonify({"status": "success"})


@app.route("/user/", methods=['GET', 'POST', 'DEL', 'PUT'])
def user():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})

    db = database_connect()
    cursor = db.cursor()

    if request.method == 'GET':
        params = request.json
        if not ("username" in params):
            return jsonify({"status": "not enough data"})

        cursor.execute("SELECT * FROM users WHERE username = " + params["username"])
        results = cursor.fetchall()
        return jsonify(results)

    if request.method == 'DEL':
        params = request.json
        if not ("username" in params):
            return jsonify({"status": "not enough data"})

        cursor.execute("DELETE FROM users WHERE username = " + params["username"])
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"status": "failure"})
        else:
            return jsonify({"status": "success"})

    if request.method == 'PUT':
        params = request.json
        if not ("name" in params and
                "surname" in params and
                "username" in params and
                "password" in params):
            return jsonify({"status": "not enough data"})


        if "avatar" not in params:
            params["avatar"] = "https://eu.ui-avatars.com/api/?name=" + params["name"] + "+" + params["surname"] + "&size=250"

        if "currency" not in params:
            params["currency"] = "PLN"

        if "city" not in params:
            params["city"] = "Warszawa"

        hashed_password = hashlib.sha256(params["password"].encode('utf-8')).hexdigest()

        sql = "INSERT INTO users (name, surname, city, currency, avatar, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (params["name"], params["surname"], params["city"], params["currency"], params["avatar"], params["username"], hashed_password)

        cursor.execute(sql, val)
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"status": "failure"})
        else:
            return jsonify({"status": "success"})

    if request.method == 'POST':
        params = request.json
        if not ("id" in params and
                "name" in params and
                "surname" in params and
                "city" in params and
                "currency" in params and
                "avatar" in params):
            return jsonify({"status": "not enough data"})

        cursor = db.cursor()
        sql = "UPDATE users SET name = %s, surname = %s, city = %s, currency = %s, avatar = %s WHERE id = %s"
        val = (params["name"], params["surname"], params["city"], params["currency"], params["avatar"], params["id"])
        cursor.execute(sql, val)
        db.commit()
        print(cursor.rowcount, "record(s) affected")
        if cursor.rowcount == 0:
            return jsonify({"status": "failure"})
        else:
            return jsonify({"status": "success"})


@app.route("/availableCities/", methods=['GET'])
def availableCities():
    file = open('Data/cities.json', encoding="utf8")
    data = json.load(file)
    return jsonify(data)


@app.route("/travelDestinations/", methods=['GET'])
def travelDestinations():
    params = request.json
    if not ("startingCity" in params and
            "weatherForecastDays" in params and
            "numberOfPeople" in params and
            "startDate" in params and
            "endDate" in params and
            "pageNumber" in params):
        return jsonify({"status": "not enough data"})

    data = getTravelDestinations(params["startingCity"], params["weatherForecastDays"], params["numberOfPeople"], params["startDate"], params["endDate"], params["pageNumber"])
    return jsonify(data)


@app.route("/fakeTravelDestinations/", methods=['GET'])
def fakeTravelDestinations():
    params = request.json
    if not ("startingCity" in params and
            "weatherForecastDays" in params and
            "numberOfPeople" in params and
            "startDate" in params and
            "endDate" in params and
            "pageNumber" in params):
        return jsonify({"status": "not enough data"})

    file = open('Data/destinations.json', encoding="utf8")
    data = json.load(file)
    return jsonify(data)


@app.route("/fakeGetFavorites/", methods=['GET'])
def fakeGetFavorites():
    params = request.json
    if not ("user_id" in params):
        return jsonify({"status": "not enough data"})
    file = open('Data/favorites.json', encoding="utf8")
    data = json.load(file)
    return jsonify(data)

