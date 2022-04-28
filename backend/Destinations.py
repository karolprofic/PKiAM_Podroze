from getData import getCityData
import json
import mpu

class Destinations:
    def __init__(self, startingLocation, weatherForecastDays, numberOfPeople, startDate, endDate, pageNumber):
        self.startingLocation = startingLocation
        self.weatherForecastDays = weatherForecastDays
        self.numberOfPeople = numberOfPeople
        self.startDate = startDate
        self.endDate = endDate
        self.pageNumber = pageNumber

    def findTravelDestinations(self):
        file = open('Data/cities.json', encoding="utf8")
        cities = json.load(file)
        cities = self.removeStartingLocation(cities["cities"])
        cities = self.addDistanceFromStartingCity(cities[0], cities[1])
        cities = sorted(cities, key=lambda element: element["distance"])
        cities = self.filterCitiesByPage(cities)

        travelDestinations = []
        for city in cities:
            travelDestinations.append(getCityData(city, self.weatherForecastDays, self.startDate, self.endDate, self.numberOfPeople))

        with open('Data/destinations.json', 'w') as file:
            json.dump(travelDestinations, file)

        return travelDestinations

    def removeStartingLocation(self, cities):
        citiesList = []
        startingCity = {}
        for city in cities:
            if city["namePL"] == self.startingLocation:
                startingCity = city
                continue
            citiesList.append(city)

        return citiesList, startingCity

    @staticmethod
    def addDistanceFromStartingCity(cities, startingCity):
        for city in cities:
            distance = mpu.haversine_distance((startingCity["latitude"], startingCity["longitude"]), (city["latitude"], city["longitude"]))
            city["distance"] = round(distance, 2)
        return cities

    def filterCitiesByPage(self, cities):
        filteredCities = []
        i = 0
        citiesPerPage = 10
        firstIndex = (self.pageNumber * citiesPerPage) - citiesPerPage
        lastIndex = self.pageNumber * citiesPerPage

        if lastIndex > len(cities):
            firstIndex = len(cities) - 10
            lastIndex = len(cities)

        for city in cities:
            if firstIndex <= i < lastIndex:
                filteredCities.append(city)
            i = i + 1

        return filteredCities
