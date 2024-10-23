import unittest
from datetime import datetime  # Import the datetime module
from src.weather_monitor import kelvin_to_celsius, calculate_daily_summary

class TestWeatherMonitor(unittest.TestCase):

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(kelvin_to_celsius(273.15), 0)
        self.assertAlmostEqual(kelvin_to_celsius(300), 26.85)

    def test_calculate_daily_summary(self):
        updates = [
            {'current_temp': 30, 'main_weather': 'Clear', 'timestamp': 1633072800},  # Day 1
            {'current_temp': 32, 'main_weather': 'Clear', 'timestamp': 1633159200},  # Day 2
            {'current_temp': 29, 'main_weather': 'Rain', 'timestamp': 1633245600},   # Day 3
        ]
        summary = calculate_daily_summary(updates)
        self.assertEqual(len(summary), 3)  # 3 unique days
        self.assertAlmostEqual(summary[datetime.fromtimestamp(1633072800).date()]['avg_temp'], 30)
        self.assertAlmostEqual(summary[datetime.fromtimestamp(1633159200).date()]['avg_temp'], 32)
        self.assertAlmostEqual(summary[datetime.fromtimestamp(1633245600).date()]['avg_temp'], 29)

if __name__ == '__main__':
    unittest.main()
