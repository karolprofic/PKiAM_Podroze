import json
from flask import Flask, request, jsonify
from destinations import getTravelDestinations
import mysql.connector

app = Flask(__name__)


def databse_connect():
    mysql_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="travel_app"
    )

    return mysql_db


#######################################################################
# TODO
#######################################################################
# Autoryzacja
# - login
# - logout
# - token is valid
#######################################################################

@app.route("/favorites/", methods=['GET', 'DEL', 'PUT'])
def favorites():
    db = databse_connect()
    cursor = db.cursor()
    if request.method == 'GET':
        params = request.json
        if not ("user_id" in params):
            return jsonify({"status": "not enough data"})

        cursor.execute("SELECT * FROM favorites WHERE user_id = " + params["user_id"])
        results = cursor.fetchall()
        return jsonify(results)

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
    db = databse_connect()
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


# Strana główna
@app.route("/availableCities/")
def availableCities():
    file = open('Data/cities.json', encoding="utf8")
    data = json.load(file)
    return jsonify(data)


# Lista potencjalnych kierunków
@app.route("/travelDestinations/")
def travelDestinations():
    startingCity = request.args.get('startingCity', "Łódź")
    weatherForecastDays = request.args.get('weatherForecastDays', 10)
    numberOfPeople = request.args.get('numberOfPeople', 1)
    startDate = request.args.get('startDate', "2022-09-30")
    endDate = request.args.get('endDate', "2022-10-01")
    pageNumber = request.args.get('pageNumber', 1)
    data = getTravelDestinations(startingCity, weatherForecastDays, numberOfPeople, startDate, endDate, pageNumber)
    return jsonify(data)


# Lista potencjalnych kierunków - bez wykorzystywania limitów
@app.route("/fakeTravelDestinations/")
def fakeTravelDestinations():
    file = open('Data/destinations.json', encoding="utf8")
    data = json.load(file)
    return jsonify(data)
