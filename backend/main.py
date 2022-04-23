import json
from flask import Flask, request, jsonify
from database import database_connect
from destinations import getTravelDestinations, getFavoritesDestinations

app = Flask(__name__)


@app.route("/favorites/", methods=['GET', 'DEL', 'PUT'])
def favorites():
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
    db = database_connect()
    cursor = db.cursor()

    if request.method == 'GET':
        params = request.json
        if not ("id" in params):
            return jsonify({"status": "not enough data"})

        cursor.execute("SELECT * FROM users WHERE id = " + params["id"])
        results = cursor.fetchall()
        return jsonify(results)

    if request.method == 'DEL':
        params = request.json
        if not ("id" in params):
            return jsonify({"status": "not enough data"})

        cursor.execute("DELETE FROM users WHERE id = " + params["id"])
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"status": "failure"})
        else:
            return jsonify({"status": "success"})

    if request.method == 'PUT':
        params = request.json
        if not ("name" in params and
                "surname" in params and
                "city" in params and
                "currency" in params and
                "avatar" in params):
            return jsonify({"status": "not enough data"})

        sql = "INSERT INTO users (name, surname, city, currency, avatar) VALUES (%s, %s, %s, %s, %s)"
        val = (params["name"], params["surname"], params["city"], params["currency"], params["avatar"])
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


#######################################################################
# TODO
#######################################################################
# Authorization
# - login
# - logout
# - token is valid
#######################################################################
