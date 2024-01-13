
# %%

#%%
import requests
import pandas as pd
import numpy as np
# Define headers and parameters

with open('tide_api_key') as f:
    api_key = f.read()


headers = {'Ocp-Apim-Subscription-Key': api_key,}

# Base URL
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
        continuous_heights = feature['properties']['ContinuousHeightsAvailable']
        
        rows.append([latitude, longitude, name, continuous_heights])

# Convert to a pandas DataFrame
        df = pd.DataFrame(rows, columns=['Latitude', 'Longitude', 'Name', 'ContinuousHeightsAvailable'])

    # Display the DataFrame

except requests.exceptions.RequestException as e:
    print(e)
