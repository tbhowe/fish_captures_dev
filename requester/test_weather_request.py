#%%
import datetime
import pandas as pd
import requests
import numpy as np


class WeatherAPI:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    
    def _fetch_data(self, endpoint):
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def _get_hourly_weather_from_timestamp(current_time, hourly_data):
        formatted_time = current_time.strftime('%Y-%m-%dT%H:00')
        matching_row = hourly_data[hourly_data['time'] == formatted_time].reset_index(drop=True)
        matching_row = matching_row.values[0]
        return_time = current_time.strftime('%Y-%m-%dT%H:%M:%S')
        matching_row[0] = return_time
        return matching_row

    def get_weather(self):
        endpoint = f"{self.BASE_URL}?latitude={self.lat}&longitude={self.lng}&hourly=temperature_2m,precipitation_probability,rain,pressure_msl,cloudcover_low,cloudcover_mid,cloudcover_high,windspeed_10m,winddirection_10m,windgusts_10m&daily=sunrise,sunset&timezone=Europe%2FLondon"
        
        data = self._fetch_data(endpoint)
        hourly_data = pd.DataFrame(data['hourly'], columns=data['hourly_units'])
        
        current_time = datetime.datetime.now()
        return self._get_hourly_weather_from_timestamp(current_time, hourly_data)


# Test
dodman_latlong = [50.220564, -4.801677]
api = WeatherAPI(dodman_latlong[0], dodman_latlong[1])
weather = api.get_weather()
print(weather)

# %%
