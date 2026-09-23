# Weather Data Engineering Pipeline

A personal data engineering project that collects weather data from the Open-Meteo REST API, transforms it, validates its quality, and prepares it for analysis.

## Technologies

- Python
- REST API
- Pandas
- DuckDB
- SQL
- JSON
- Parquet
- Pytest
- Git

## Pipeline

1. Fetches current weather data for selected cities.
2. Stores raw API responses as timestamped JSON files.
3. Transforms nested JSON into a structured Pandas DataFrame.
4. Validates required columns, missing values, and valid data ranges.
5. Saves processed data in Parquet format.
6. Performs analytical queries using Pandas and DuckDB SQL.
7. Tests the transformation logic with Pytest.

## Data Source

Weather data is collected from the [Open-Meteo API](https://open-meteo.com/).

## Future Improvements

- Store data in Amazon S3.
- Use AWS Glue for data cataloging and transformation.
- Query cloud data with Amazon Athena.
- Automate ingestion with AWS Lambda and EventBridge.
- Monitor pipeline execution with Amazon CloudWatch.
