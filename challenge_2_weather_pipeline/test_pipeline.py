import pandas as pd
from weather_pipeline import clean_data, compute_daily_averages

def test_clean_data():
    df = pd.DataFrame({
        "humidity": [50, -5, 110, 80],
        "min_temp": [10, 10, 10, 10],
        "max_temp": [20, 20, 20, 20]
    })
    cleaned = clean_data(df)
    assert all(cleaned["humidity"].between(0, 100)), "Humidity out of bounds"

def test_compute_daily_averages():
    df = pd.DataFrame({
        "min_temp": [10, 15],
        "max_temp": [20, 25]
    })
    df = compute_daily_averages(df)
    assert "avg_temp" in df.columns
    assert df["avg_temp"].tolist() == [15.0, 20.0]
