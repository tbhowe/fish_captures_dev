#%%
import requests
import numpy as np
from datetime import datetime, timedelta

class SunTimeAPI:
    BASE_URL = "https://api.sunrise-sunset.org/json"
    
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    
    def fetch_data(self, date=None, formatted=1):
        params = {
            'lat': self.lat,
            'lng': self.lng,
            'formatted': formatted
        }
        if date:
            params['date'] = date
        
        response = requests.get(self.BASE_URL, params=params)
        return response.json()
    
    @staticmethod
    def extract_times(data):
        if data['status'] != 'OK':
            print(f"Error: {data['status']}")
            return None
        
        results = data['results']
        times_keys = [
            "sunrise", "sunset",
            "civil_twilight_begin", "civil_twilight_end",
            "nautical_twilight_begin", "nautical_twilight_end",
            "astronomical_twilight_begin", "astronomical_twilight_end"
        ]
        
        return np.array([results[key] for key in times_keys])

    @staticmethod
    def adjust_for_dst(date_str):
        """
        Adjusts for UK daylight saving time.
        Adds 1 hour if the date is in DST.
        """
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        last_sunday_march = max(datetime(date_obj.year, 3, i) for i in range(25, 32))
        last_sunday_october = max(datetime(date_obj.year, 10, i) for i in range(25, 32))

        if last_sunday_march <= date_obj < last_sunday_october:
            return timedelta(hours=1)
        return timedelta()

    def get_sun_times(self,date,formatted=1):
        '''Method to return the sun times for a given date.'''
        data = self.fetch_data(date, formatted)
        times_array = self.extract_times(data)
        
        if times_array is not None:
            dst_adjustment = api.adjust_for_dst(date if date else datetime.utcnow().strftime('%Y-%m-%d'))
            adjusted_times = [(datetime.strptime(time, "%I:%M:%S %p") + dst_adjustment).time().strftime("%I:%M:%S %p") for time in times_array]
            return np.array(adjusted_times)
        return None
    
    def get_column_headings(self):
        """Method to fetch the column headings from the API response."""
        # Fetching a sample data to extract keys
        data = self.fetch_data()
        if data['status'] != 'OK':
            print(f"Error: {data['status']}")
            return None
        return list(data['results'].keys())

# Test
lat = 36.7201600
lng = -4.4203400
api=SunTimeAPI(lat, lng)
times_array = api.get_sun_times(date="2023-09-08")
print(times_array)

# %%
