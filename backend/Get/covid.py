import requests
import json

# Unlimited / month
# 60 requests per minute
API_COVID_URL = "https://covid-193.p.rapidapi.com/statistics"
API_COVID_KEY = "29eefaae15mshfb32eab96aade47p18cf99jsn3e2b70595940"
API_COVID_HOST = "covid-193.p.rapidapi.com"


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
