from ThreadWithResult import ThreadWithResult
import requests
import json

# Unlimited / month
# 60 requests per minute
API_COVID_URL = "https://covid-193.p.rapidapi.com/statistics"
API_COVID_KEY = "29eefaae15mshfb32eab96aade47p18cf99jsn3e2b70595940"
API_COVID_HOST = "covid-193.p.rapidapi.com"

# 490 / month
# 5 requests per minute
API_BOOKING_URL = "https://booking-com.p.rapidapi.com/v1/hotels/search"
API_BOOKING_KEY = "29eefaae15mshfb32eab96aade47p18cf99jsn3e2b70595940"
API_BOOKING_HOST = "booking-com.p.rapidapi.com"

# 500 / month
# 10 requests per minute
API_WEATHER_URL = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
API_WEATHER_KEY = "29eefaae15mshfb32eab96aade47p18cf99jsn3e2b70595940"
API_WEATHER_HOST = "community-open-weather-map.p.rapidapi.com"

def convertToInt(data):
    if data is None:
        return 0
    else:
        return int(data)


def getCovidStatistics(countryName):
    headers = {
        "X-RapidAPI-Host": API_COVID_HOST,
        "X-RapidAPI-Key": API_COVID_KEY
    }

    response = requests.request("GET", API_COVID_URL, headers=headers)
    response = json.loads(response.text)

    countriesList = response["response"]

    covidInfo = {}

    for country in countriesList:
        if country["country"] == countryName:
            covidInfo = {
                "casesNew": convertToInt(country["cases"]["new"]),
                "casesActive": convertToInt(country["cases"]["active"]),
                "casesCritical": convertToInt(country["cases"]["critical"]),
                "casesRecovered": convertToInt(country["cases"]["recovered"]),
                "casesPerOneMillion": convertToInt(country["cases"]["1M_pop"]),
                "casesTotal": convertToInt(country["cases"]["total"]),
                "deathsNew": convertToInt(country["deaths"]["new"]),
                "deathsPerOneMillion": convertToInt(country["deaths"]["1M_pop"]),
                "deathsTotal": convertToInt(country["deaths"]["total"]),
                "testsPerOneMillion": convertToInt(country["tests"]["1M_pop"]),
                "testsTotal": convertToInt(country["tests"]["total"]),
            }
            break

    return covidInfo


def getHotelsInCity(checkInDate, checkoutDate, numberOfPeople, cityID):

    querystring = {
        "room_number": "1",
        "checkin_date": checkInDate,
        "filter_by_currency": "PLN",
        "order_by": "popularity",
        "adults_number": numberOfPeople,
        "locale": "en-gb",
        "dest_type": "city",
        "dest_id": cityID,
        "units": "metric",
        "checkout_date": checkoutDate,
        "include_adjacency": "true",
        "categories_filter_ids": "class::2,class::4,free_cancellation::1",
        "page_number": "0",
    }

    headers = {
        "X-RapidAPI-Host": API_BOOKING_HOST,
        "X-RapidAPI-Key": API_BOOKING_KEY
    }

    response = requests.request("GET", API_BOOKING_URL, headers=headers, params=querystring)
    response = json.loads(response.text)

    hotels = []
    for hotel in response["result"]:
        hotel = {
            "name": hotel["hotel_name"],
            "address": hotel["address_trans"],
            "score": hotel["review_score"],
            "url": hotel["url"],
            "image": hotel["max_photo_url"],
            "price": hotel["min_total_price"],
            "currency": hotel["currencycode"]
        }
        hotels.append(hotel)

    countryCode = response["result"][0]["cc1"]
    cityName = response["result"][0]["city_name_en"]
    data = {
        "numberOfHotels": response["unfiltered_count"],
        "bookingURL": "https://www.booking.com/city/ " + countryCode + "/" + cityName + ".html",
        "hotels": hotels
    }

    return data


def getWeatherForecast(numberOfDays, locationLatitude, locationLongitude):
    querystring = {
        "lat": locationLatitude,
        "lon": locationLongitude,
        "cnt": numberOfDays,
        "units": "metric"
    }

    headers = {
        "X-RapidAPI-Host": API_WEATHER_HOST,
        "X-RapidAPI-Key": API_WEATHER_KEY
    }

    response = requests.request("GET", API_WEATHER_URL, headers=headers, params=querystring)
    response = json.loads(response.text)

    daysForecast = response["list"]
    daysWhetherInfo = []
    for dayForecast in daysForecast:
        dayWhetherInfo = {
            "unixTime": int(dayForecast["dt"]),
            "dayTemperature": float(dayForecast["temp"]["day"]),
            "weatherIcon": dayForecast["weather"][0]["main"]
        }
        daysWhetherInfo.append(dayWhetherInfo)

    return daysWhetherInfo

def getCityData(city, weatherForecastDays, startDate, endDate, numberOfPeople):
    covidThread = ThreadWithResult(target=getCovidStatistics, args=(city["country"],))
    weatherThread = ThreadWithResult(target=getWeatherForecast, args=(weatherForecastDays, city["latitude"], city["longitude"],))
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

    cityData = {
        "name": city["namePL"],
        "imageURL": city["image"],
        "bookingURL": hotelsData["bookingURL"],
        "numberOfHotels": hotelsData["numberOfHotels"],
        "distance": city["distance"],
        "weather": weatherData,
        "covid": covidData,
        "hotels": hotelsData["hotels"]
    }
    return cityData
