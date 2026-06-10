import boto3
import requests
import json
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)


class EarthquakeManager:

    def __init__(self, urls):
        self._urls = urls

    def get_eq_data(
        self,
    ):
        url = self._urls[0]
        resp = requests.get(url)
        resp.raise_for_status()
        daily_eq = resp.json()
        # pprint.pprint(dict(daily_eq).keys())
        features = daily_eq["features"]
        # pprint.pprint(features[0])
        eq_today = []
        for feature in features:
            id = feature.get("id", None)
            properties = feature.get("properties", {})
            mag = properties.get("mag", float("-inf"))
            place = properties.get("place", None)
            time = properties.get("time", None)
            seconds = time // 1000
            time_dt = datetime.fromtimestamp(seconds)
            time_str = datetime.strftime(time_dt, "%Y-%m-%dT%H:%M:%SZ")
            eq_today.append({"id": id, "mag": mag, "place": place, "time": time_str})
        return eq_today


if __name__ == "__main__":
    earthquake_manager = EarthquakeManager(
        ["https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"]
    )
    eq_data = earthquake_manager.get_eq_data()
    sorted_eq = sorted(eq_data, key=lambda x: x["mag"], reverse=True)
    pp.pprint(sorted_eq)
