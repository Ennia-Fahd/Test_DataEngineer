# Technical Documentation – Weather Pipeline

## 🎯 Goal

Build a data processing pipeline that fetches weather data for 5 major cities using OpenWeatherMap's `/day_summary` API.

---

## 🔄 Pipeline Steps

### 1. Data Ingestion

- Fetch daily weather data for the past 30 days for each city.
- API endpoint: `https://api.openweathermap.org/data/3.0/onecall/day_summary`
- Collected fields: min/max temperature, noon humidity, total precipitation.

### 2. Cleaning & Transformation

- Remove missing values.
- Filter humidity values to stay within 0–100%.
- Compute daily average temperature:
  ```
  avg_temp = (min_temp + max_temp) / 2
  ```

### 3. Storage

- Store processed data into SQLite (`weather_data.sqlite`):
  - Table `daily_weather` – daily weather per city
  - Table `cities` – list of cities

### 4. Analysis

- Aggregate by city:
  - Average temperature
  - Average humidity
  - Total precipitation
  - Count of rainy days (precipitation > 0)

- Display insights:
  - Hottest / Coldest city
  - Global average temperature
  - City with most rainy days

### 5. Visualization

- Generate a line chart of temperature trends over 30 days using `matplotlib`
- File generated: `temperature_trend.png`

### 6. Reporting

- Generate summary CSV report: `weather_report.csv`

---

## 📁 Output Files

- `weather_data.sqlite` – processed SQLite database
- `weather_report.csv` – analytical report
- `temperature_trend.png` – line chart visualization
- `weather.log` – execution log

---

## 🧪 Unit Testing

- `test_pipeline.py` includes tests for `clean_data()` and `compute_daily_averages()`
- Framework used: `pytest`

---

## 📌 Limitations

- Requires paid access to `/day_summary` endpoint from OpenWeatherMap
- Hardcoded to 5 major global cities
