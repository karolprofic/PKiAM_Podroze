import json
from Get.covid import getCovidStatistics
from flask import Flask, request, jsonify
from destinations import getTravelDestinations

app = Flask(__name__)
#######################################################################
# TODO
#######################################################################
# Autoryzacja
# - login
# - logout
# - token is valid
#######################################################################
# Ulubione
# - PUT | Dodaj do ulubionych (userID, cityData)
# - DEL | Usuń z ulubionych (userID, cityIdentyficator)
# - GET | Pobierz wszystko z ulubionych (userID)
#######################################################################
# Użytkownik
# - GET  | Zwróć dane użytkownika (userID)
# - PUT  | Dodaj nowego użytkownika (userData)
# - DEL  | Usuń użytkownika (userID)
# - POST | Uaktualnij dane użytkownika (userID, userData)
#######################################################################

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

