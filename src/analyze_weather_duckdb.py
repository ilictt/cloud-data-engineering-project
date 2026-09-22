import duckdb


weather_summary = duckdb.sql("""
    SELECT
        city,
        AVG(temperature_c) AS average_temperature,
        AVG(wind_speed_kmh) AS average_wind_speed
    FROM 'data/processed/weather_processed.parquet'
    GROUP BY city
    ORDER BY average_temperature DESC
""")

print("Weather summary:")
print(weather_summary)

windiest_city = duckdb.sql("""
    SELECT city
    FROM 'data/processed/weather_processed.parquet'
    GROUP BY city
    ORDER BY AVG(wind_speed_kmh) DESC
    LIMIT 1
""").fetchone()[0]

print("Windiest city:")
print(windiest_city)