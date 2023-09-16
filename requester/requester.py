#%%
import requests
import pandas as pd

class GenerateRecord:
    '''Main class for concatenating API calls and then generating a record from them'''
    def __init__(self, url, data):
        pass

class APIRequest:

    '''Base Class for API Requests.'''
    

    def __init__(self, endpoint):
        self.endpoint = endpoint

    @property
    def url(self):
        if self.BASE_URL is None:
            raise NotImplementedError("BASE_URL should be specified in the subclass.")
        return f"{self.BASE_URL}/{self.endpoint}"

    def prepare_params(self):
        """
        Prepare the parameters required for the API call.
        To be implemented by the subclass if necessary.
        """
        return {}

    def process_response(self, response):
        """
        Process the API response.
        To be implemented by the subclass if necessary.
        """
        return response.json()

    def get(self):
        ''' The base GET request method.'''
        params = self.prepare_params()
        response = requests.get(self.endpoint, params=params)

        # Ensure the request was successful
        response.raise_for_status()

        return self.process_response(response)

class TestWeatherAPI(APIRequest):

    def __init__(self, endpoint):
        super().__init__(endpoint)




dodman_latlong = [50.220564,-4.801677]
example_endpoint = f'https://api.open-meteo.com/v1/forecast?latitude={dodman_latlong[0]}&longitude={dodman_latlong[0]}&hourly=temperature_2m,precipitation_probability,rain,pressure_msl,cloudcover_low,cloudcover_mid,cloudcover_high,windspeed_10m,winddirection_10m,windgusts_10m&daily=sunrise,sunset&timezone=Europe%2FLondon'
test = requests.get(example_endpoint)
print(type(test.json()))
print(test.json().keys())
hourly = pd.DataFrame(test.json()['hourly'])
daily = pd.DataFrame(test.json()['daily'])

hourly.head()


# %%
