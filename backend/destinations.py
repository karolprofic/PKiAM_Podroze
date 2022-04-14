import json
import mpu

from Thread.ThreadWithResult import ThreadWithResult
from Get.covid import getCovidStatistics
from Get.hotel import getHotelsInCity
from Get.weather import getWeatherForecast


def distanceBetweenTwoPoints(firstLatitude, firstLongitude, secondLatitude, secondLongitude):
    return mpu.haversine_distance((firstLatitude, firstLongitude), (secondLatitude, secondLongitude))


def removeStartingLocation(cities, startingLocation):
    citiesList = []
    startingCity = {}
    for city in cities:
        if city["namePL"] == startingLocation:
            startingCity = city
            continue
        citiesList.append(city)

    return citiesList, startingCity


def addDistanceFromStartingCity(cities, startingCity):
    for city in cities:
        distance = distanceBetweenTwoPoints(startingCity["latitude"], startingCity["longitude"], city["latitude"],
                                             city["longitude"])
        city["distance"] = round(distance, 2)
    return cities


def filterCitiesByPage(cities, pageNumber):
    filteredCities = []
    i = 0
    citiesPerPage = 10
    firstIndex = (pageNumber * citiesPerPage) - citiesPerPage
    lastIndex = pageNumber * citiesPerPage

    if lastIndex > len(cities):
        firstIndex = len(cities) - 10
        lastIndex = len(cities)

    for city in cities:
        if firstIndex <= i < lastIndex:
            filteredCities.append(city)
        i = i + 1

    return filteredCities


def getTravelDestinations(startingLocation, weatherForecastDays, numberOfPeople, startDate, endDate, pageNumber):
    file = open('Data/cities.json', encoding="utf8")
    cities = json.load(file)
    cities = removeStartingLocation(cities["cities"], startingLocation)
    cities = addDistanceFromStartingCity(cities[0], cities[1])
    cities = sorted(cities, key=lambda city: city["distance"])
    cities = filterCitiesByPage(cities, pageNumber)

    data = []
    for city in cities:
        covidThread = ThreadWithResult(target=getCovidStatistics, args=(city["country"],))
        weatherThread = ThreadWithResult(target=getWeatherForecast,args=(weatherForecastDays, city["latitude"], city["longitude"],))
        hotelsThread = ThreadWithResult(target=getHotelsInCity, args=(startDate, endDate, numberOfPeople, city["nameBooking"],))

        covidThread.start()
        weatherThread.start()
        hotelsThread.start()

        covidThread.join()
        weatherThread.join()
        hotelsThread.join()

        covidData = covidThread.result
        weatherData = weatherThread.result
        hotelsData = hotelsThread.result

        listElement = {
            "name": city["namePL"],
            "imageURL": city["image"],
            "bookingURL": hotelsData["bookingURL"],
            "numberOfHotels": hotelsData["numberOfHotels"],
            "distance": city["distance"],
            "weather": weatherData,
            "covid": covidData,
            "hotels": hotelsData["hotels"]
        }
        data.append(listElement)

    with open('Data/destinations.json', 'w') as newFile:
        json.dump(data, newFile)

    return data


getTravelDestinations("Łódź", 4, 2, "2022-09-30", "2022-10-01", 1)
