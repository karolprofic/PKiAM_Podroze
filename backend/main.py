import json
from Get.covid import getCovidStatistics
from flask import Flask, request, jsonify

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


