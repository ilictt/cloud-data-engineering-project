import json
from datetime import datetime, timezone
from pathlib import Path

import requests

#dictionary of the cities and their coordinates
CITIES = { 
    "nis": {"latitude": 43.3209, "longitude": 21.8958},
    "belgrade": {"latitude": 44.7866, "longitude": 20.4489},
    "london": {"latitude": 51.5074, "longitude": -0.1278},
}


def fetch_weather(city_name, coordinates):
    url = "https://api.open-meteo.com/v1/forecast"

    parameters = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",
    }

    response = requests.get(url, params=parameters, timeout=30)
    response.raise_for_status()

    return {
        "city": city_name,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "weather_data": response.json(),
    }


def main():
    project_root = Path(__file__).resolve().parents[1]
    raw_data_folder = project_root / "data" / "raw"
    raw_data_folder.mkdir(parents=True, exist_ok=True)

    collected_data = []

    for city_name, coordinates in CITIES.items():
        print(f"Fetching weather data for {city_name}...")
        city_data = fetch_weather(city_name, coordinates)
        collected_data.append(city_data)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_file = raw_data_folder / f"weather_{timestamp}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(collected_data, file, indent=4)

    print(f"Raw data saved to: {output_file}")


if __name__ == "__main__":
    main()