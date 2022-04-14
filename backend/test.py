import json

from covid import getCovidStatistics
from helpers import distanseBeetweenTwoPoints
from hotel import getHotelsInCity
from weather import getWeatherForecast

file = open('cities.json', encoding="utf8")



cities = json.load(file)

print(distanseBeetweenTwoPoints(52.2296756, 21.0122287, 52.406374, 16.9251681))


numberOfDays = 4
numberOfPeople = 2
startDate = "2022-09-30"
endDate = "2022-10-01"

for city in cities["cities"]:
    weatherData = getWeatherForecast(numberOfDays, city["latitude"], city["longitude"])
    hotelsData = getHotelsInCity(startDate, endDate, numberOfPeople, "-553173")
    covidData = getCovidStatistics(city["country"])
    data = {
        "name": city["namePL"],
        "image": city["image"],
        "weather": weatherData,
        "covid": covidData,
        "bookingURL": hotelsData["bookingURL"],
        "numberOfHotels": hotelsData["numberOfHotels"],
        "hotels": hotelsData["hotels"]
    }

    print(json.dumps(data, indent=2))

    break

