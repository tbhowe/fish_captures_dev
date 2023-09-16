#%%
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TideStation:
    BASE_URL = 'https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations'

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {'Ocp-Apim-Subscription-Key': self.api_key,}
        self.df_stations = self._get_tide_stations_dataframe()

    def _get_tide_stations_dataframe(self):
        try:
            response = requests.get(self.BASE_URL, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            rows = [
                [feature['geometry']['coordinates'][1],
                 feature['geometry']['coordinates'][0],
                 feature['properties']['Name'],
                 feature['properties']['Id'],
                 feature['properties']['ContinuousHeightsAvailable']]
                for feature in data['features']
            ]

            return pd.DataFrame(rows, columns=['Latitude', 'Longitude', 'Name', 'id', 'ContinuousHeightsAvailable'])
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    @staticmethod
    def _haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return R * c
    
    @staticmethod
    def tide_cycle_time(target_timestamp: str, tide_data: list) -> str:
        # Convert the target timestamp to a datetime object
        target_dt = datetime.fromisoformat(target_timestamp)

        # Combine both LowWater and HighWater events and sort them
        tide_times = sorted(
            tide_data, 
            key=lambda x: datetime.fromisoformat(x['DateTime'])
        )

        # Find the nearest tide time
        nearest_tide_event = min(tide_times, key=lambda event: abs(datetime.fromisoformat(event['DateTime']) - target_dt))
        
        nearest_tide_time = datetime.fromisoformat(nearest_tide_event['DateTime'])

        # Calculate the difference
        difference = target_dt - nearest_tide_time

        # If the nearest event is a HighWater, infer the time since the previous LowWater
        half_cycle = timedelta(hours=6, minutes=12, seconds=30)  # Approximate duration between LW and HW
        if nearest_tide_event['EventType'] == 'HighWater' and difference.total_seconds() < 0:
            difference = half_cycle + difference

        # Return the difference in the format HH:MM:SS
        hours, remainder = divmod(difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def closest_station(self, lat, lon):
        self.df_stations['distance'] = self._haversine(lat, lon, self.df_stations['Latitude'], self.df_stations['Longitude'])
        closest = self.df_stations[self.df_stations['ContinuousHeightsAvailable'] == True].nsmallest(1, 'distance')
        return closest[['Name', 'id']]

    def get_tide_data(self, station_id: str):
        endpoint = f'{self.BASE_URL}/{station_id}/TidalEvents?duration=1'
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

if __name__ == '__main__':
    with open('tide_api_key') as f:
        API_KEY = f.read().strip()
    ts = TideStation(API_KEY)

    given_lat, given_lon = 50.220564, -4.801677
   
    station = ts.closest_station(given_lat, given_lon).iloc[0]

    tide_data = ts.get_tide_data(station['id'])
    current_time = datetime.utcnow()
    print(ts.tide_cycle_time(current_time.isoformat(), tide_data))

    print(tide_data[0]['Height'])

# %%
