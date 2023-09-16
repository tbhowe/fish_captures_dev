#%%

import requests
import pandas as pd
import numpy as np

def get_tide_stations_dataframe(api_key):
    """
    Returns a DataFrame containing tide stations information.

    Parameters:
    - api_key (str): The API key to authenticate with the Admiralty Tidal API.

    Returns:
    - df (pd.DataFrame): DataFrame containing tide stations information.
    """
    
    headers = {'Ocp-Apim-Subscription-Key': api_key,}
    base_url = 'https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations'

    try:
        # Make the GET request
        response = requests.get(base_url, headers=headers)

        # Check the response
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()

        # Extract the necessary values
        rows = []
        for feature in data['features']:
            longitude, latitude = feature['geometry']['coordinates']
            name = feature['properties']['Name']
            id = feature['properties']['Id']
            continuous_heights = feature['properties']['ContinuousHeightsAvailable']
            
            rows.append([latitude, longitude, name, id, continuous_heights])

        # Convert to a pandas DataFrame
        df = pd.DataFrame(rows, columns=['Latitude', 'Longitude', 'Name', 'id', 'ContinuousHeightsAvailable'])
        return df

    except requests.exceptions.RequestException as e:
        print(e)
        return None



def haversine(lat1, lon1, lat2, lon2):
    """Calculates Haversine distance between two sets of coordinates."""
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Compute differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

def closest_station(df, lat, lon):
    """Computes Closest Tide Station"""
    # Compute distance for each station
    df['distance'] = haversine(lat, lon, df['Latitude'], df['Longitude'])

    # Filter for ContinuousHeightsAvailable and find the station with the minimum distance
    closest = df[df['ContinuousHeightsAvailable'] == True].nsmallest(1, 'distance')
    
    return closest[['Name','id']]



def get_tide_data(station_id: str):
    """
    Returns a DataFrame containing tide stations information.

    Parameters:
    - station (str): The name of the tide station to get data for.

    Returns:
    - df (pd.DataFrame): DataFrame containing tide stations information.
    """
    headers = {'Ocp-Apim-Subscription-Key': api_key,}
    station_id = str(station['id'].values[0])
    print(station_id)
    endpoint = f'https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/{station_id}/TidalEvents?duration=1'
    response = requests.get(endpoint, headers=headers)
    tide_data = response.json()
    return tide_data

if __name__ == '__main__':
    # Get tide stations DataFrame
    with open('tide_api_key') as f:
        api_key = f.read()
    df = get_tide_stations_dataframe(api_key)
    given_lat, given_lon = 50.220564, -4.801677
    station = closest_station(df, given_lat, given_lon)
    
    tide_data = get_tide_data(station['id'])
    print(f'tide_data for {station["Name"]}')
    print(tide_data)

# %%
