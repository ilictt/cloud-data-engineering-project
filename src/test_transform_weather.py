from src.transform_weather import transform_weather_data


def test_transform_weather_data_creates_one_row_per_city():
    raw_data = [
        {
            "city": "nis",
            "retrieved_at": "2026-09-22T10:00:00+00:00",
            "weather_data": {
                "latitude": 43.3209,
                "longitude": 21.8958,
                "current": {
                    "time": "2026-09-22T10:00",
                    "temperature_2m": 20.5,
                    "relative_humidity_2m": 55,
                    "wind_speed_10m": 12.3,
                },
            },
        },
        {
            "city": "belgrade",
            "retrieved_at": "2026-09-22T10:00:00+00:00",
            "weather_data": {
                "latitude": 44.7866,
                "longitude": 20.4489,
                "current": {
                    "time": "2026-09-22T10:00",
                    "temperature_2m": 21.0,
                    "relative_humidity_2m": 60,
                    "wind_speed_10m": 10.5,
                },
            },
        },
    ]

    transformed_rows = transform_weather_data(raw_data)

 #assert means that the test will fail if the condition is not met
    assert len(transformed_rows) == 2
    assert transformed_rows[0]["city"] == "nis"
    assert transformed_rows[0]["temperature_c"] == 20.5
    assert transformed_rows[1]["city"] == "belgrade"