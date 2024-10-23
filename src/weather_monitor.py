import requests
import time
import json
import os
import logging
import argparse
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Ensure it's used in a non-interactive environment
import matplotlib.pyplot as plt
import pandas as pd

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = '6b155d0a0416cba8293e1343da2f58ac'  # Replace with your actual OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
URL = "http://api.openweathermap.org/data/2.5/weather"

# Default threshold (used for tests)
THRESHOLD_TEMP = 35.0

def fetch_weather_data(city):
    """Fetch weather data from OpenWeatherMap API."""
    logging.info(f"Fetching data for {city}")
    try:
        response = requests.get(URL, params={'q': city, 'appid': API_KEY})
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {e}")
        return None

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def process_weather_data(data):
    """Process the fetched weather data to extract relevant information."""
    main_weather = data['weather'][0]['main']
    current_temp = kelvin_to_celsius(data['main']['temp'])
    feels_like = kelvin_to_celsius(data['main']['feels_like'])
    return {
        'main_weather': main_weather,
        'current_temp': current_temp,
        'feels_like': feels_like,
        'timestamp': data['dt']
    }

def calculate_daily_summary(weather_updates):
    """Calculate daily weather summaries from collected updates."""
    summary = {}
    for update in weather_updates:
        date = datetime.fromtimestamp(update['timestamp']).date()
        if date not in summary:
            summary[date] = {
                'max_temp': update['current_temp'],
                'min_temp': update['current_temp'],
                'total_temp': update['current_temp'],
                'count': 1,
                'conditions': [update['main_weather']]
            }
        else:
            summary[date]['max_temp'] = max(summary[date]['max_temp'], update['current_temp'])
            summary[date]['min_temp'] = min(summary[date]['min_temp'], update['current_temp'])
            summary[date]['total_temp'] += update['current_temp']
            summary[date]['count'] += 1
            summary[date]['conditions'].append(update['main_weather'])
            
    for date, data in summary.items():
        data['avg_temp'] = data['total_temp'] / data['count']
        # Determine dominant condition (most frequent)
        data['dominant_condition'] = max(set(data['conditions']), key=data['conditions'].count)

    return summary

def check_alerts(weather_updates):
    """Check if any weather updates exceed the defined thresholds."""
    for update in weather_updates:
        if update['current_temp'] > THRESHOLD_TEMP:
            logging.warning(f"Alert! {update['current_temp']}°C exceeds threshold at {datetime.fromtimestamp(update['timestamp'])}")

def visualize_weather_summary(daily_summary):
    """Visualize daily weather summary."""
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')

    plt.figure(figsize=(10, 6))
    
    dates = list(daily_summary.keys())
    avg_temps = [summary['avg_temp'] for summary in daily_summary.values()]

    plt.plot(dates, avg_temps, marker='o', label='Average Temperature')
    plt.title('Daily Average Temperature')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.savefig('visualizations/daily_weather_summary.png')  # Save the figure in the visualizations folder
    plt.close()

def save_to_csv(weather_updates, filename='weather_updates.csv'):
    """Save weather updates to a CSV file."""
    df = pd.DataFrame(weather_updates)

    try:
        existing_data = pd.read_csv(filename)
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv(filename, index=False)
    logging.info(f"Weather updates saved to {filename}")

def main():
    weather_updates = []
    logging.info("Starting weather monitoring.")
    try:
        while True:
            for city in CITIES:
                data = fetch_weather_data(city)
                if data:
                    processed_data = process_weather_data(data)
                    processed_data['city'] = city
                    weather_updates.append(processed_data)
                    logging.info(f"Processed data: {processed_data}")

            if weather_updates:
                daily_summary = calculate_daily_summary(weather_updates)
                logging.info(f"Daily Summary: {daily_summary}")
                visualize_weather_summary(daily_summary)  # Visualize daily summaries
                save_to_csv(weather_updates)  # Save updates to CSV
                
                check_alerts(weather_updates)  # Check for alerts
            
            weather_updates = []  # Clear updates for the next iteration
            time.sleep(300)  # Wait for 5 minutes
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Weather Monitoring Script')
    parser.add_argument('--threshold', type=float, default=35.0, help='Temperature threshold for alerts')
    args = parser.parse_args()
    THRESHOLD_TEMP = args.threshold

    main()
