# Weather Data Pipeline – OpenWeatherMap

This project downloads, processes, analyzes, and stores weather data for 5 major cities over the past 30 days using OpenWeatherMap's `/day_summary` API.

## ✅ Requirements

- Python 3.9+
- OpenWeatherMap API key with access to "One Call by Call"
- `docker` (optional for containerized execution)

## 📦 Installing Dependencies (Local)

```bash
pip install -r requirements.txt
```

## ▶️ Run Locally

```bash
python weather_pipeline.py
```

The following files will be generated:
- `weather_report.csv` – final report
- `weather_data.sqlite` – local SQLite database
- `temperature_trend.png` – temperature trend chart
- `weather.log` – execution log file

## 🐳 Run with Docker

```bash
docker build -t weather-pipeline .
docker run --rm -v ${PWD}:/app weather-pipeline
```

## 🧪 Run Unit Tests

```bash
pytest test_pipeline.py
```
