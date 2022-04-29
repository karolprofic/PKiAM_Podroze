from getData import getCityData
import datetime
import json

class Favorites:
    def __init__(self, listOfCities):
        self.listOfCities = listOfCities
        self.weatherForecastDays = 10
        self.numberOfPeople = 1
        self.startDate = datetime.date.today()
        self.endDate = self.startDate + datetime.timedelta(days=10)

    def getFavoritesDestinations(self):
        file = open('data/cities.json', encoding="utf8")
        cities = json.load(file)
        cities = self.completeCitiesData(cities["cities"])

        favoritesDestinations = []
        for city in cities:
            favoritesDestinations.append(getCityData(city, self.weatherForecastDays, self.startDate, self.endDate, self.numberOfPeople))

        with open('data/favorites.json', 'w') as file:
            json.dump(favoritesDestinations, file)

        return favoritesDestinations

    def completeCitiesData(self, cities):
        favouriteCities = []

        for city in cities:
            for cityName in self.listOfCities:
                if city["namePL"] == cityName:
                    city["distance"] = 0
                    favouriteCities.append(city)
        return favouriteCities
