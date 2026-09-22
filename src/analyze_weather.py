import pandas as pd

weather_df = pd.read_parquet(
    "data/processed/weather_processed.parquet"
) 

average_temperature = (
    weather_df
    .groupby("city")["temperature_c"]
    .mean()
    .sort_values(ascending=False)
)

print("Average temperature by city:")
print(average_temperature)

windiest_city = (
    weather_df
    .groupby("city")["wind_speed_kmh"]
    .mean()
    .idxmax()
)

print(f"Windiest city: {windiest_city}")