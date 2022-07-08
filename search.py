import os
import shodan


class Scanner:
    def __init__(self):
        self.SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
        if self.SHODAN_API_KEY == None:
            raise KeyError("Shodan API key not found")
        self.api = shodan.Shodan(self.SHODAN_API_KEY)

    def search(self, query):
        try:
            return self.api.search(query)
        except shodan.APIError as e:
            print(f'Error: {e}')
