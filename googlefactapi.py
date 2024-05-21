import requests
from dotenv import load_dotenv
import os
import json
load_dotenv()

claims = [
    "Climate Change",
    "Abortion"
]

presets = {
    'languageCode': 'en-us',
    'maxAgeDays': None,
    'pageSize': None,
    'offset': None,
}


class GoogleApi:
    def __init__(self) -> None:
        self.key = os.getenv('GOOGLE_KEY')
        self.url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'
        # https://toolbox.google.com/factcheck/api/search other url thats not public technically
    
    def search_claim(self,query,singleUse=True):
        params = {
        'query': query,
        'key': self.key
        }
        
        for key, value in presets.items():
            if value is not None:
                params[key] = value
        
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            if not singleUse:
                return response.json()
            else:
                filename = f'search_claim_{query}.json'
                with open(filename, 'w') as outfile:
                    json.dump(response.json(), outfile)
        
    def group_search_claims(self,querys):
        count = 0
        filename = f'group_search_{count}.json'
        while os.path.exists(filename):
            count += 1
            filename = f"group_search_{count}.json"
        
        group_results = {}
        for claim in querys:
            data = self.search_claim(claim, singleUse=False)
            if data:
                group_results[claim] = data
        
        with open(filename, 'w') as outputfile:
            json.dump(group_results, outputfile)

api = GoogleApi()
api.group_search_claims(claims)