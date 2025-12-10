import os
import requests
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"

LAT = os.environ.get("LAT", "59.94")
LON = os.environ.get("LON", "30.32")

REQUEST_COUNTER = Counter(
    "weather_requests_total",
    "Total HTTP requests to weather app",
    ["endpoint"]
)

def get_current_temperature():
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current_weather": "true"
    }
    resp = requests.get(BASE_URL, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    return data["current_weather"]["temperature"]

@app.route("/")
def index():
    REQUEST_COUNTER.labels(endpoint="/").inc()
    temp = get_current_temperature()
    return f"<h1>Current temperature: {temp} °C</h1>"

@app.route("/weather")
def weather():
    REQUEST_COUNTER.labels(endpoint="/weather").inc()
    temp = get_current_temperature()
    return jsonify({"temperature_c": temp})

@app.route("/health")
def health():
    return "OK", 200

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
