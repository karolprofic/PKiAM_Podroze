import json
import requests

# 490 / month
# 5 requests per minute
API_BOOKING_URL = "https://booking-com.p.rapidapi.com/v1/hotels/search"
API_BOOKING_KEY = "29eefaae15mshfb32eab96aade47p18cf99jsn3e2b70595940"
API_BOOKING_HOST = "booking-com.p.rapidapi.com"


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
