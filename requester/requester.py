import requests

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
