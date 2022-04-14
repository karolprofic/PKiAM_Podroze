import requests
import json
from covid import getCovidStatistics
from weather import getWeatherForecast
from helpers import distanseBeetweenTwoPoints
from flask import Flask, request, jsonify
from markupsafe import escape

app = Flask(__name__)

# Uwierzytelnianie
# @app.route("/login")
# def login():
#     return jsonify({'Tresc': "Logowanie"})
#
# @app.route("/logout")
# def logout():
#     return jsonify({'Tresc': "Wylogowywanie"})

# Użytkownik
@app.route('/users/<user_id>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def users(user_id):
    if request.method == 'GET':
        return jsonify({'Tresc': "Zwrócono dane uzytkownika"})
    if request.method == 'POST':
        # username = request.form.get('username')
        # password = request.form.get('password')
        # city = request.form.get('city')
        # currency = request.form.get('currency')
        return jsonify({'Tresc': "Uaktualnienie danych uzytkownika"})
    if request.method == 'PUT':
        return jsonify({'Tresc': "Dodano nowego uzytkownika"})
    if request.method == 'DELETE':
        return jsonify({'Tresc': "Usunieto uzytkownika"})
    else:
        return jsonify({'Tresc': "Błąd"})

# Ulubione
@app.route('/favourites/delete', methods = ['POST'])
def deleteFromFavourites():
    id = request.get_json().get('id')

@app.route('/favourites/<user_id>', methods = ['GET', 'PUT', 'DELETE'])
def favourites(user_id):
    if request.method == 'GET':
        return jsonify({'Tresc': "Zwrócono wszystkie ulubione miejsca dla konkretnego uzytkownika"})
    if request.method == 'PUT':
        return jsonify({'Tresc': "Dodano miejsce do ulubionych uzytkownika"})
    if request.method == 'DELETE':
        return jsonify({'Tresc': "Usunięto miejsce z ulubionych uzytkownika"})
    else:
        return jsonify({'Tresc': "Błąd"})

# Strana główna
@app.route("/availableCities/")
def availableCities():
    return jsonify({'Tresc': "Strona główna"})

# Lista potencjalnych kierunków
@app.route("/travelDestinations/")
def travelDestinations():
    startDate = request.args.get('startDate', None)
    endDate = request.args.get('endDate', None)
    startingCity = request.args.get('startingCity', "Łódź")
    numberOfPeople = request.args.get('numberOfPeople', 1)
    pageNumber = request.args.get('pageNumber', 1)
    return jsonify({'Miasto startowe': startingCity})



print(json.dumps(getCovidStatistics("Czechia"), indent=2))
# print(json.dumps(getWeatherForecast(10, 37.773972, -122.431297), indent=2)) # los angeles
# print(distanseBeetweenTwoPoints(52.2296756, 21.0122287, 52.406374, 16.9251681))


# TODO:
# - Booking API - hotels etc.
# - ?? Informacje o mieście, jakieś zdjęcia, atrakcje?


