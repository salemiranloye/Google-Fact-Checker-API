import requests
from dotenv import load_dotenv
import os
import json
import spacy
nlp = spacy.load("en_core_web_sm")

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

whitelist_pos = {"PROPN","VERB"}


class GoogleApi:
    def __init__(self) -> None:
        self.key = os.getenv('GOOGLE_KEY')
        self.url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'
        # https://toolbox.google.com/factcheck/api/search other url thats not public technically

    def decontruct(self,sentence):
        tokenized = nlp(sentence)
        stripped = []
        for token in tokenized:
            if not token.is_stop and token.pos_ in whitelist_pos:
                stripped.append(token.text)

        return ' '.join(stripped)

    def search_claim(self,query,singleUse=True):
        query = self.decontruct(query)
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
api.search_claim("Trump deported fewer people than Barack Obama did when he was president.")