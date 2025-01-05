import os
import requests
import json
import pandas as pd
import io

from pandas import json_normalize
from pandas.core.interchange.dataframe_protocol import DataFrame

# TODO: Connect Last.fm API

USER_AGENT = os.environ["USER_AGENT"]
API_KEY = os.environ["API_KEY"]

class Lastfm_ctrl:

    def __init__(self):
        pass

    # Request to Last.fm to get a list of similar artist based on the query entered
    def thing (self, var):
        pass

    def lastfm_get(self, payload):

        # define headers and URL
        headers = {'user-agent' : USER_AGENT}
        url = 'http://ws.audioscrobbler.com/2.0'

        # add API key and format the payload
        payload['api_key'] = API_KEY
        payload['format'] = 'json'

        response = requests.get(url, headers= headers, params= payload)
        return  response

    # used for testing and to make the results easier to read
    def print_json(self, obj):
        text = json.dumps(obj, sort_keys=True, indent= 4)
        print(text)

    # the seach function of this API is not ideal as it has a chance of putting the correct artist down the JSON List
    # need to make a function that compares the results and accurately selects the correct artist
    def search_artist(self, artist):
        response = self.lastfm_get({'method': ' artist.search', 'artist': artist})
        # j = response.json()
        dict = []
        for a in response.json()['results']['artistmatches']['artist']:
            dict.append(
                {
                    'name': a['name'],
                    'url': a['url']
                }
            )

        return dict

    # take the result of the query and loop through them and convert them into a pandas data dictionary
    def get_similar_artists(self, artist):
        response = self.lastfm_get({'method': ' artist.getSimilar', 'artist': artist, 'limit': 250 })
        dict = []
        for a in response.json()['similarartists']['artist']:
            dict.append(
                {
                    'name': a['name'],
                    'match': a['match'],
                    'url': a['url']
                }
            )
        # self.print_json(response.json())
        return dict

# input to enter artist
# obj = Lastfm_ctrl()
# artist = input("Please enter the name of an artist: ")
# dict = obj.to_dict(artist)
# print(type(obj.search_artist(artist)))
# obj.print_json(obj.search_artist(artist))

# df = pd.DataFrame(dict)
# print(df)