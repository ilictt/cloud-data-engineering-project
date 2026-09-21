#the point is to  transform the json file into the table
# 1. Pronađi najnoviji raw JSON fajl
# 2. Otvori ga
# 3. Učitaj JSON u Python
# 4. Prođi kroz svaki grad
# 5. Izvuci podatke iz weather_data → current
# 6. Napravi ravne redove
# 7. Pretvori redove u Pandas DataFrame
# 8. Sačuvaj rezultat kao Parquet u data/processed

import json
from pathlib import Path
import pandas as pd

#finding the main folder of the project
project_root = Path(__file__).resolve().parents[1]
raw_data_folder = project_root / "data" / "raw"

#looking for all data files starting with "weather_" and ending with ".json" in the raw data folder
raw_files = sorted(raw_data_folder.glob("weather_*.json"))
if not raw_files:
    raise FileNotFoundError("No raw JSON files found in the 'data/raw' directory.") 
latest_raw_file = raw_files[-1]

#opening the latest raw JSON file and loading its content into the python variable
with latest_raw_file.open("r", encoding="utf-8") as file:
    raw_data = json.load(file) #transform the JSON into a Python object (list of dictionaries)

print(f"Loaded {len(raw_data)} city records")

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

#transforming the list of dictionaries into a Pandas DataFrame and saving it as a Parquet file in the processed data folder

weather_df = pd.DataFrame(transformed_rows)
print(weather_df) #need to see table in the terminal to check if everything is correct

#deciding where to store the data
processed_data_folder = project_root / "data" / "processed"
processed_data_folder.mkdir(parents=True, exist_ok=True)

output_file=processed_data_folder / "weather_processed.parquet" #just name
weather_df.to_parquet(output_file, index=False) #storing the data in parquet format

print(f"Processed data saved to: {output_file}")