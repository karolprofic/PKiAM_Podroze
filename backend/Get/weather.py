import requests
import json

# 500 / month
# 10 requests per minute
API_WEATHER_URL = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
API_WEATHER_KEY = "29eefaae15mshfb32eab96aade47p18cf99jsn3e2b70595940"
API_WEATHER_HOST = "community-open-weather-map.p.rapidapi.com"


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
