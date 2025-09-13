import requests
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import logging
import matplotlib.pyplot as plt

# 🔧 Configuration du logging
logging.basicConfig(filename='weather.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = "b1d129ab9f7c69c140209a70f909f7e6"

CITIES = {
    "Paris": (48.8566, 2.3522),
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
    "Tokyo": (35.6895, 139.6917),
    "Casablanca": (33.5899, -7.6039)
}

BASE_URL = "https://api.openweathermap.org/data/3.0/onecall/day_summary"

def get_weather(lat, lon, date_str):
    url = f"{BASE_URL}?lat={lat}&lon={lon}&date={date_str}&units=metric&appid={API_KEY}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return {
            "date": data["date"],
            "min_temp": data["temperature"]["min"],
            "max_temp": data["temperature"]["max"],
            "humidity": data["humidity"]["afternoon"],
            "precipitation": data.get("precipitation", {}).get("total", 0)
        }
    except Exception as e:
        logging.error(f"Error for {lat},{lon} on {date_str}: {e}")
        return None

def collect_weather_data():
    all_data = []
    for city, (lat, lon) in CITIES.items():
        logging.info(f"Downloading data for {city}")
        for i in range(30):
            date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
            data = get_weather(lat, lon, date)
            if data:
                data["city"] = city
                all_data.append(data)
    return pd.DataFrame(all_data)

def clean_data(df):
    return df.dropna().loc[df["humidity"].between(0, 100)]

def compute_daily_averages(df):
    df["avg_temp"] = (df["min_temp"] + df["max_temp"]) / 2
    return df

def store_to_sqlite(df):
    conn = sqlite3.connect("weather_data.sqlite")
    df.to_sql("daily_weather", conn, if_exists="replace", index=False)
    pd.DataFrame(df["city"].unique(), columns=["city"]).to_sql("cities", conn, if_exists="replace", index=False)
    conn.close()

def analyze(df):
    summary = df.groupby("city").agg({
        "avg_temp": "mean",
        "humidity": "mean",
        "precipitation": ["sum", lambda x: (x > 0).sum()]
    }).reset_index()
    summary.columns = ["city", "avg_temp", "avg_humidity", "total_precipitation", "rainy_days"]
    return summary

def plot_temperature_trend(df):
    plt.figure(figsize=(10, 6))
    for city in df["city"].unique():
        city_df = df[df["city"] == city]
        plt.plot(city_df["date"], city_df["avg_temp"], label=city)
    plt.xlabel("Date")
    plt.ylabel("Average Temperature (°C)")
    plt.title("Temperature Trend (30 days)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("temperature_trend.png")
    logging.info("Plot saved as temperature_trend.png")

def export_report(summary):
    summary.to_csv("weather_report.csv", index=False)
    logging.info("CSV report exported.")

def print_insights(summary, df):
    hottest = summary.loc[summary["avg_temp"].idxmax()]
    coldest = summary.loc[summary["avg_temp"].idxmin()]
    overall_avg = df["avg_temp"].mean()
    most_rainy = summary.loc[summary["rainy_days"].idxmax()]
    
    print(f"🌡️ Hottest city: {hottest['city']} ({hottest['avg_temp']:.2f}°C)")
    print(f"❄️ Coldest city: {coldest['city']} ({coldest['avg_temp']:.2f}°C)")
    print(f"🌍 Overall average temperature: {overall_avg:.2f}°C")
    print(f"☔ Most rainy days: {most_rainy['city']} ({most_rainy['rainy_days']} days)")

if __name__ == "__main__":
    raw_data = collect_weather_data()
    if raw_data.empty:
        logging.warning("No data collected.")
        print("❌ No data collected.")
    else:
        clean_df = clean_data(raw_data)
        clean_df = compute_daily_averages(clean_df)
        store_to_sqlite(clean_df)
        summary_df = analyze(clean_df)
        export_report(summary_df)
        plot_temperature_trend(clean_df)
        print_insights(summary_df, clean_df)
        print("✅ Pipeline completed.")
