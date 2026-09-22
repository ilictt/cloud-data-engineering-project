#the point is to  transform the json file into the table

import json
from pathlib import Path

import pandas as pd


def find_latest_raw_file(project_root):
    raw_data_folder = project_root / "data" / "raw"

    raw_files = sorted(raw_data_folder.glob("weather_*.json"))

    if not raw_files:
        raise FileNotFoundError("No raw weather files found.")

    return raw_files[-1]


def load_raw_data(raw_file):
    with raw_file.open("r", encoding="utf-8") as file:
        return json.load(file)

def transform_weather_data(raw_data):
    transformed_rows = []

    for city_record in raw_data:
        city = city_record["city"]
        retrieved_at = city_record["retrieved_at"]
        weather_data = city_record["weather_data"]
        current_weather = weather_data["current"]

        row = {
            "city": city,
            "retrieved_at": retrieved_at,
            "observation_time": current_weather["time"],
            "latitude": weather_data["latitude"],
            "longitude": weather_data["longitude"],
            "temperature_c": current_weather["temperature_2m"],
            "humidity_percent": current_weather["relative_humidity_2m"],
            "wind_speed_kmh": current_weather["wind_speed_10m"],
        }

        transformed_rows.append(row)

    return transformed_rows 

def validate_weather_data(weather_df):
    required_columns = [
        "city",
        "retrieved_at",
        "observation_time",
        "latitude",
        "longitude",
        "temperature_c",
        "humidity_percent",
        "wind_speed_kmh",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in weather_df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    print("Required column check passed.")

    expected_cities = {"nis", "belgrade", "london"}
    actual_cities = set(weather_df["city"])

    missing_cities = expected_cities - actual_cities

    if missing_cities:
        raise ValueError(f"Missing cities: {missing_cities}")

    if weather_df["temperature_c"].isna().any():
        raise ValueError("Temperature values are missing.")

    if weather_df["humidity_percent"].isna().any():
        raise ValueError("Humidity values are missing.")

    if not weather_df["humidity_percent"].between(0, 100).all():
        raise ValueError("Humidity must be between 0 and 100.")

    if weather_df["wind_speed_kmh"].isna().any():
        raise ValueError("Wind speed values are missing.")

    if (weather_df["wind_speed_kmh"] < 0).any():
        raise ValueError("Wind speed cannot be negative.")

    print("All data quality checks passed.")
    

def save_processed_data(weather_df, project_root):
    processed_data_folder = project_root / "data" / "processed"
    processed_data_folder.mkdir(parents=True, exist_ok=True)

    output_file = processed_data_folder / "weather_processed.parquet"

    weather_df.to_parquet(output_file, index=False)

    return output_file

def main():
    project_root = Path(__file__).resolve().parents[1]

    latest_raw_file = find_latest_raw_file(project_root)
    raw_data = load_raw_data(latest_raw_file)
    transformed_rows = transform_weather_data(raw_data)

    weather_df = pd.DataFrame(transformed_rows)
    validate_weather_data(weather_df)

    print(weather_df)

    output_file = save_processed_data(weather_df, project_root)

    print(f"Processed data saved to: {output_file}")


if __name__ == "__main__":
    main()