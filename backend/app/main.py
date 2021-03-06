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


config = {
    'origins': '*',
    'methods': ['OPTIONS', 'GET', 'POST'],
    'allow_headers': ['Authorization', 'Content-Type'],
    'supports_credentials': True
}

# CORS(app, resources={
#     r"/api/*" : config
# })

def requestHaveRequiredParameters(requiredParams, listOfParams):
    for param in requiredParams:
        if param not in listOfParams:
            return True
    return False

def database_connect():
    mysql_db = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="travel_app"
    )
    return mysql_db

# For testing
@app.route('/main/', methods=['POST'])
@cross_origin(**config)
def main():
    return jsonify({'status': 'main page or login/logout redirection'})

@app.route('/api/login', methods=['POST'])
@cross_origin(**config)
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
                # return redirect('/main/')
                return jsonify({'status': 'logged successfully'})

            else:
                return jsonify({'status': 'wrong password'})
        else:
            return jsonify({'status': 'wrong login'})
    else:
        return jsonify({'status': 'wrong login and password'})


@app.route('/api/logout', methods=['POST'])
@cross_origin(**config)
def logout():
    if 'username' in session:
        session.pop('username', None)
    # return redirect('/main/')
    return jsonify({'status': 'logout successfully'})

@app.route("/api/getFavorites", methods=['POST'])
@cross_origin(**config)
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


@app.route("/api/removeFavorite", methods=['POST'])
@cross_origin(**config)
def removeFavorite():
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


@app.route("/api/addFavorites", methods=['POST'])
@cross_origin(**config)
def addFavorites():
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



@app.route("/api/getUser", methods=['GET'])
@cross_origin(**config)
def getUser():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})
    db = database_connect()
    cursor = db.cursor()
    # params = request.json
    # print(params)
    # requiredParams = ["username"]

    # if requestHaveRequiredParameters(requiredParams, params):
    #     return jsonify({"status": "not enough data"})

    cursor.execute("SELECT * FROM users WHERE username = '" + session["username"] + "'")
    results = cursor.fetchall()
    return jsonify(results)


@app.route("/api/removeUser", methods=['POST'])
@cross_origin(**config)
def removeUser():
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



@app.route("/api/addUser", methods=['POST'])
@cross_origin(**config)
def addUser():
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

@app.route("/api/updateUser", methods=['POST'])
@cross_origin(**config)
def updateUser():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'})
    db = database_connect()
    cursor = db.cursor()
    params = request.json
    requiredParams = ["id", "name", "surname", "city", "currency", "avatar", "username"]

    if requestHaveRequiredParameters(requiredParams, params):
        return jsonify({"status": "not enough data"})

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


@app.route("/api/availableCities", methods=['POST'])
@cross_origin(**config)
def availableCities():
    file = open('data/cities.json', encoding="utf8")
    data = json.load(file)
    return jsonify(data)


@app.route("/api/travelDestinations", methods=['POST'])
@cross_origin(**config)
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
