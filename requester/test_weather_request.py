#%%
import datetime
import pandas as pd
import requests
import numpy as np
import time

start_time = time.time()
def get_weather_data(endpoint):
    current_time = datetime.datetime.now()
    response = requests.get(endpoint)
    response.raise_for_status()

    data = response.json()
    hourly_data = pd.DataFrame(data['hourly'], columns=data['hourly_units'])
    daily_data = pd.DataFrame(data['daily'], columns=data['daily_units'])

    matching_row_hourly = get_hourly_weather_from_timestamp(current_time, hourly_data)
    matching_row_daily = get_daily_weather_from_timestamp(current_time, daily_data)

    # Appending everything but the timestamp from the second array into the first array
    combined_data = np.append(matching_row_hourly, matching_row_daily[1:])

    print(combined_data)

def get_hourly_weather_from_timestamp(current_time, hourly_data):
    formatted_time = current_time.strftime('%Y-%m-%dT%H:00')
    matching_row = hourly_data[hourly_data['time'] == formatted_time].reset_index(drop=True)
    matching_row = matching_row.values[0]
    return_time = current_time.strftime('%Y-%m-%dT%H:%M:%S')
    matching_row[0] = return_time

    return matching_row

def get_daily_weather_from_timestamp(current_time, daily_data):
    formatted_date_str = current_time.strftime('%Y-%m-%d')
    matching_row_daily = daily_data[daily_data['time'] == formatted_date_str].reset_index(drop=True)
    matching_row_daily = matching_row_daily.values[0]
    return_date = current_time.strftime('%Y-%m-%dT%H:%M:%S')
    matching_row_daily[0] = return_date

    return matching_row_daily

dodman_latlong = [50.220564,-4.801677]
example_endpoint = f'https://api.open-meteo.com/v1/forecast?latitude={dodman_latlong[0]}&longitude={dodman_latlong[1]}&hourly=temperature_2m,precipitation_probability,rain,pressure_msl,cloudcover_low,cloudcover_mid,cloudcover_high,windspeed_10m,winddirection_10m,windgusts_10m&daily=sunrise,sunset&timezone=Europe%2FLondon'
get_weather_data(example_endpoint)
print("--- %s seconds ---" % (time.time() - start_time))

# %%
