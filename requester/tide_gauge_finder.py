#%%
import requests

api_root ='http://environment.data.gov.uk/flood-monitoring/id/stations?type=TideGauge'
lat = 50.220564
long = -4.801677
d = 50
query = f'?lat={lat}&long={long}&dist={d}'
full_query=f'https://environment.data.gov.uk/flood-monitoring/id/stations?type=TideGauge&lat={lat}&long={long}&dist={d}'
response = requests.get(full_query)
print(response)
# %%
