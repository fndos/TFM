import os
import shodan
import json
from time import time
from datetime import datetime
from tkinter.messagebox import showerror
import fnc


class ShodanEngine:
    def __init__(self):
        self.token = os.getenv("SHODAN_API_KEY")
        if self.token == None:
            raise KeyError("Shodan API key not found")
        self.api = shodan.Shodan(self.token)
        self.last_time = ''
        self.last_total = ''
        self.last_query = ''
        self.last_response = None

    def search(self, query):
        try:
            start_time = time()
            response = self.api.search(query)
            end_time = time()
            self.last_time = round(end_time - start_time, 2)
            self.last_query = query
            self.last_total = fnc.get('total', response)
            self.last_response = response
            self.has_failed = False
            timestamp = int(datetime.now().timestamp())
            with open(f'data/response_{timestamp}.json', 'w') as outfile:
                json.dump(response, outfile)
            return response
        except shodan.APIError as error:
            showerror(title='Error', message=error)
            self.has_failed = True

    def build_query(self, search, filter):
        return f'{search} {"net:" + filter if filter else ""}'
