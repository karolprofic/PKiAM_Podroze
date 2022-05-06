import hashlib
import mysql.connector
import json
from flask import Flask, request, jsonify, session
from werkzeug.utils import redirect
from Destinations import Destinations
from Favorites import Favorites
from flask_cors import CORS, cross_origin
from flask_session import Session

DEVELOPMENT_MODE = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pkiam-podroze'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

def requestHaveRequiredParameters(requiredParams, listOfParams):
    for param in requiredParams:
        if param not in listOfParams:
            return True
    return False

def database_connect():
    mysql_db = mysql.connector.connect(
        # host="db",
        # user="root",
        # password="root",
        # database="travel_app"
        host="localhost",
        user="root",
        password="",
        database="travel_app"
    )
    return mysql_db

@app.route('/')
@cross_origin(supports_credentials=True)
def main():
    return jsonify({'status': 'login/logout successfully'})

@app.route('/login/', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    params = request.json
    if params['username'] and params['password']:
        db = database_connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '" + params["username"] + "'")
        row = cursor.fetchone()
        if len(row) > 0:
            password = row[7]
            hashed_password = hashlib.sha256(params["password"].encode('utf-8')).hexdigest()
            if password == hashed_password:
                session['username'] = params["username"]
                return redirect('/')
            else:
                return jsonify({'status': 'wrong password'})
        else:
            return jsonify({'status': 'wrong login'})
    else:
        return jsonify({'status': 'wrong login and password'})


@app.route('/logout/', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect('/')

@app.route("/getFavorites/", methods=['POST'])
@cross_origin(supports_credentials=True)
def getFavorites():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})

    db = database_connect()
    cursor = db.cursor()
    params = request.json
    requiredParams = ["user_id"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    if DEVELOPMENT_MODE:
        file = open('data/favorites.json', encoding="utf8")
        data = json.load(file)
        return jsonify(data)
    else:
        cursor.execute("SELECT * FROM favorites WHERE user_id = '" + params["user_id"] + "'")
        results = cursor.fetchall()
        listOfCites = []
        for i in results:
            listOfCites.append(i[2])
        fav = Favorites(listOfCites)
        return jsonify(fav.getFavoritesDestinations())


@app.route("/delFavorites/", methods=['POST'])
@cross_origin(supports_credentials=True)
def delFavorites():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})

    db = database_connect()
    cursor = db.cursor()
    params = request.json
    requiredParams = ["user_id", "city"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    sql = "DELETE FROM favorites WHERE user_id = %s AND city = %s"
    val = (params["user_id"], params["city"])
    cursor.execute(sql, val)
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"status": "failure"})
    else:
        return jsonify({"status": "success"})


@app.route("/putFavorites/", methods=['POST'])
@cross_origin(supports_credentials=True)
def putFavorites():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})

    db = database_connect()
    cursor = db.cursor()
    params = request.json
    requiredParams = ["user_id", "city"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    sql = "INSERT INTO favorites (user_id, city) VALUES (%s, %s)"
    val = (params["user_id"], params["city"])
    cursor.execute(sql, val)
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"status": "failure"})
    else:
        return jsonify({"status": "success"})



@app.route("/getUser/", methods=['POST'])
@cross_origin(supports_credentials=True)
def getUser():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})
    db = database_connect()
    cursor = db.cursor()
    params = request.json
    print(params)
    requiredParams = ["username"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    cursor.execute("SELECT * FROM users WHERE username = '" + params["username"] + "'")
    results = cursor.fetchall()
    return jsonify(results)


@app.route("/delUser/", methods=['POST'])
@cross_origin(supports_credentials=True)
def delUser():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})
    db = database_connect()
    cursor = db.cursor()
    params = request.json
    requiredParams = ["username"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    cursor.execute("DELETE FROM users WHERE username = '" + params["username"] + "'")
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"status": "failure"})
    else:
        return jsonify({"status": "success"})



@app.route("/putUser/", methods=['POST'])
@cross_origin(supports_credentials=True)
def putUser():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})
    db = database_connect()
    cursor = db.cursor()
    params = request.json
    requiredParams = ["name", "surname", "username", "password"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    if "avatar" not in params:
        params["avatar"] = "https://eu.ui-avatars.com/api/?name=" + params["name"] + "+" + params["surname"] + "&size=250"

    if "currency" not in params:
        params["currency"] = "PLN"

    if "city" not in params:
        params["city"] = "Warszawa"

    hashed_password = hashlib.sha256(params["password"].encode('utf-8')).hexdigest()

    sql = "INSERT INTO users (name, surname, city, currency, avatar, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (params["name"], params["surname"], params["city"], params["currency"], params["avatar"], params["username"],
           hashed_password)

    cursor.execute(sql, val)
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"status": "failure"})
    else:
        return jsonify({"status": "success"})

@app.route("/postUser/", methods=['POST'])
@cross_origin(supports_credentials=True)
def postUser():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})
    db = database_connect()
    cursor = db.cursor()
    params = request.json
    requiredParams = ["id", "name", "surname", "city", "currency", "avatar", "username"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    cursor = db.cursor()
    sql = "UPDATE users SET name = %s, surname = %s, city = %s, currency = %s, avatar = %s, username = %s WHERE id = %s"
    val = (params["name"], params["surname"], params["city"], params["currency"], params["avatar"], params["username"],
           params["id"])
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record(s) affected")
    if cursor.rowcount == 0:
        return jsonify({"status": "failure"})
    else:
        return jsonify({"status": "success"})


@app.route("/availableCities/", methods=['POST'])
@cross_origin(supports_credentials=True)
def availableCities():
    file = open('data/cities.json', encoding="utf8")
    data = json.load(file)
    return jsonify(data)


@app.route("/travelDestinations/", methods=['POST'])
@cross_origin(supports_credentials=True)
def travelDestinations():
    params = request.json
    requiredParams = ["startingCity", "weatherForecastDays", "numberOfPeople", "startDate", "endDate", "pageNumber"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

    if DEVELOPMENT_MODE:
        file = open('data/destinations.json', encoding="utf8")
        data = json.load(file)
        return jsonify(data)
    else:
        destinations = Destinations(params["startingCity"], params["weatherForecastDays"], params["numberOfPeople"], params["startDate"], params["endDate"], params["pageNumber"])
        return jsonify(destinations.findTravelDestinations())


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
