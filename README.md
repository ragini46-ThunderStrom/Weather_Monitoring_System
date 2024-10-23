# Weather_Monitoring_System

## Overview
The Weather Monitoring System retrieves and processes real-time weather data for major cities in India. It provides daily summaries, alerts for significant temperature changes, and visualizations to help users understand weather trends.

## Features
- Fetches real-time weather data from OpenWeatherMap API.
- Processes weather data for multiple cities.
- Calculates daily summaries, including maximum, minimum, average temperatures, and dominant weather conditions.
- Alerts users when the temperature exceeds a user-defined threshold.
- Saves weather updates to a CSV file for historical tracking.
- Visualizes daily weather summaries using Matplotlib.

  ## Technologies Used
- Python
- Requests library for API calls
- Pandas for data manipulation and storage
- Matplotlib for data visualization
- OpenWeatherMap API for weather data

  ## Setup Instructions
1. **Clone the Repository**:
   ```bash
   cd weather_monitoring

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv

3. **Activate the Virtual Environment**
    ```bash
    venv\Scripts\activate

4. **Install Required Packages**
    ```bash
    pip install requests pandas matplotlib

5. **Set Up OpenWeatherMap API Key**
- Obtain an API key from OpenWeatherMap.
- Replace the placeholder in the code with your actual API key.

## Usage
### Testing
**To run the unit tests, use the following command**
    ```bash
    python -m unittest discover tests
Implemented unit tests to ensure the reliability of the data processing and alert mechanisms.
Test cases cover the following functionalities:
Data retrieval and processing
Daily summary calculations
Alert triggers based on temperature thresholds

### Run the weather monitoring script with an optional temperature threshold argument
    ```bash
    python src/weather_monitor.py --threshold <value> "example:value=35"

## Data Processing
The system processes the fetched weather data to extract:

- Main weather condition
- Current temperature (converted from Kelvin to Celsius)
- Feels-like temperature (also converted)
- Timestamp of the data retrieval

## Alert System
The system checks if the current temperature exceeds the defined threshold and prints a warning alert in the console when an alert is triggered.

## Visualization
The daily weather summary is visualized using Matplotlib:

- The average temperature for each day is plotted, with the figure saved as daily_weather_summary.png
