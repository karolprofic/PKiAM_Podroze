import json

from _mysql_connector import MySQL

from Get.covid import getCovidStatistics
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
# Ulubione
# - POST | Dodaj do ulubionych (userID, cityData)
# - DEL  | Usuń z ulubionych (userID, cityIdentyficator)
# - GET  | Pobierz wszystko z ulubionych (userID)
#######################################################################
# Użytkownik
# - GET  | Zwróć dane użytkownika (userID)
# - PUT  | Dodaj nowego użytkownika (userData)
# - DEL  | Usuń użytkownika (userID)
# - POST | Uaktualnij dane użytkownika (userID, userData)
#######################################################################

# CREATE TABLE `travel_app`.`users` ( `id` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `surname` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `city` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `currency` VARCHAR(3) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `avatar` VARCHAR(1024) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
# CREATE TABLE `travel_app`.`favorites` ( `id` INT NOT NULL AUTO_INCREMENT , `user_id` INT NOT NULL , `city` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
# INSERT INTO `users` (`id`, `name`, `surname`, `city`, `currency`, `avatar`) VALUES (NULL, 'Jan', 'Kowalski', 'Łódź', 'PLN', 'https://cdn.pixabay.com/photo/2018/08/28/12/41/avatar-3637425__340.png');


@app.route("/favorites/", methods=['GET', 'POST', 'DEL'])
def favorites():
    params = None
    if request.method == 'GET':
        params = request.json
    if request.method == 'DEL':
        params = request.json
    if request.method == 'POST':
        params = request.json


@app.route("/user/", methods=['GET', 'POST', 'DEL', 'PUT'])
def user():
    params = None
    db = databse_connect()
    cursor = db.cursor()
    if request.method == 'GET':
        params = request.json
        cursor.execute("SELECT * FROM users WHERE id = " + params.id)
        results = cursor.fetchall()
        return jsonify(results)
    if request.method == 'DEL':
        params = request.json
        cursor.execute("DELETE FROM users WHERE id = " + params.id)
        results = cursor.fetchall()
        return jsonify(results)
    if request.method == 'PUT':
        params = request.json
    if request.method == 'POST':
        params = request.json


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

