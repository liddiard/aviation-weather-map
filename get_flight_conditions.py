from urllib import request
import json

from utils import get_flight_category


def parse_weather(metars):
    """given a list of metars, return a dict keyed by ICAO airport code,
    containing the fields we care about for the map
    """
    weather = {}
    # retrieve flying conditions from the service response and store in a
    # dictionary for each airport
    for metar in metars:
        airport = metar["icaoId"]
        weather[airport] = {
            "flight_category": get_flight_category(metar),
            "wind_speed": metar.get("wspd", 0),
            "wind_gust": metar.get("wgst", 0)
        }
    return weather

def get_weather(airports, hours_before_now=2):
    """given a list of airports, make a request to the aviation weather
    server, parse the response, and return a list of METARs
    """
    # https://aviationweather.gov/data/api/
    url = f"https://aviationweather.gov/api/data/metar?format=json&hours={hours_before_now}&ids=" + ",".join([item for item in airports if item != "NULL"])
    content = request.urlopen(url, timeout=30).read()
    return parse_weather(json.loads(content))


