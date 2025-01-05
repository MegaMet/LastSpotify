# Target: Music web app that goes though last.fm and plays music on spotify that is not in the user's library based off similar artist or songs that the user searches for.
# ---
# Select a song or artist that exist in the user's library or provide option to search via text.
# Search last.fm for the selected query
# Select similar artist to the selected query
# Select the top X number of songs by that artist
# Search Spotify for the selected songs and add them the queue.
# If a selected song is not listed; make a note of it to allow the user to reasearch it on their own and move on to the next song.
# If a selected artist is not listed; make a note of them to allow the user to reasearch it on their own.
# Allow option to allow user to select how many artist to search for and how many songs to pic from each artist.
# Rabit hole mode: Give option to add song to favorites. If the user favorites a song, it will start a new query based off that artist and repeat the same process as above.
# --- Save a list trail of songs that led to the most recent favorited song.
# Music list exporter: allow the user to export out a list of their entire favorited library in text form.
# True Random number Shuffle: Spotify shuffle sucks. Select a random number between 0 and the number of favorited song and add that song to the queue.
# --- Optional: If user skips a song that appears on the shuffle; option checkbox 1: remove that artist from the queue if there and possible showing up on the shuffle; option checkbox 2: remove songs with similar tags from the queue and possible showing up on the shuffle.
import re
from functools import total_ordering
from operator import index
from re import search
from symtable import Class

# Basic Requirements:
# ---
# Spotify API key.
# Last.FM API key.
# User Spotify signin.

# UI Requirements:
# ---
# Login screen
# Scrollable area with songs / albums / artist / playlist with a search box
# Search box for general queries
# Main area to show artist and songs
# A queue list of upcoming and songs that were added to the queue. With the first item that is actively playing showing a focus listing at the top with the album cover.by

# TODO: Generate 50 number between 0 and x; Play the songs corresponding to those numbers to the play queue

# Search for music in Last.fm
# TODO: Create a search query function that looks for artist in Last.fm

# Compare similar artist to artist that is already in user's favorites
# TODO: Get the top (int y) number of artist similar to the queried searched artist

# TODO: Compare the artist found to artist in user's favorites and ignore any matches.

# TODO: Select the first (int z) number of songs for artist that do not match and add them to the queue


import pandas as pd
import random
import os

# TODO: Connect Spotify API
# CLIENTID = "environment variable SPOTIPY_CLIENT_ID"
# CLIENT_SECRET = "environment variable SPOTIPY_CLIENT_SECRET"
import spotipy
from redis.commands.search.reducers import count
from spotipy.oauth2 import SpotifyOAuth



class Spotify_ctrl:

    def __init__(self):
        self.SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
        self.SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
        self.SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
        self.scope = "user-follow-read user-library-read playlist-modify-public user-read-playback-state user-modify-playback-state ugc-image-upload"

        self.sp_oauth = SpotifyOAuth(
            client_id= self.SPOTIPY_CLIENT_ID,
            client_secret= self.SPOTIPY_CLIENT_SECRET,
            redirect_uri= self.SPOTIPY_REDIRECT_URI,
            scope=self.scope
        )

        # if (self.sp_oauth.get_cached_token()):
        #     print("Cached token found")
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)
        # else:
        #     print("no cached token")

    #User's music
    #TODO: Create function that gets the user's music and puts it into a list

    #Shuffle play user's music
    def user_track_count(self):
        results = self.sp.current_user_saved_tracks()

        total_tracks = results['total']
        return total_tracks

    def get_random_tracks(self):
        #setting pandas dataframe columns
        song_features_list = [
            "artist", "album", "track_name", "track_id"
        ]
        tracks_df = pd.DataFrame(columns=song_features_list)

        #user authentication sign in and application access
        scope = "user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        user_track_count = self.user_track_count()

        loops = 50
        for i in range(loops):
            offset = random.randrange(user_track_count)
            results = sp.current_user_saved_tracks(offset= offset, limit= 1)
            track_features = {}
            for idx, item in enumerate(results['items']):
                track = item['track']
                track_features['track_name'] = track["name"]
                track_features['artist'] = track["album"]["artists"][0]["name"]
                track_features['album'] = track["album"]["name"]
                track_features['track_id'] = track['id']
                # audio_features = sp.audio_features(track_features['track_id'])[0]

                track_df = pd.DataFrame(track_features, index=[0])
                tracks_df = pd.concat([tracks_df, track_df], ignore_index=True)

        return tracks_df

    # def add_track_to_queue(track_uri_list):
    #     for track in track_uri_list:
    #         self.sp.add_to_queue(uri= track)

    def get_followed_artist(self):
        results = self.sp.current_user_followed_artists()

        return results

    def search_artist(self, artist, **kwargs):
        limit = kwargs.get('limit', 10)
        country_codes = ['AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO',
                         'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID', 'IE', 'IT', 'JP',
                         'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH',
                         'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY']


        results = self.sp.search(q= 'artist:' + artist, type='artist', limit= limit, market= country_codes)
        artists = results['artists']['items']
        if len(artists) > 0:
            return  artists

    # does not work as the function from spotipy 'artist_related_artists' or related throws an error: 401 message: "No token provided"
    def get_similar_artists(self, artist_id):
        results = self.sp.artist_related_artists(artist_id= artist_id)
        print(results)
        # auth_manager = SpotifyOAuth(
        #     client_id=self.SPOTIPY_CLIENT_ID,
        #     client_secret=self.SPOTIPY_CLIENT_SECRET,
        #     redirect_uri=self.SPOTIPY_REDIRECT_URI
        # )
        # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        #     client_id= self.SPOTIPY_CLIENT_ID,
        #     client_secret= self.SPOTIPY_CLIENT_SECRET,
        #     redirect_uri= self.SPOTIPY_REDIRECT_URI
        # ))
        # auth_url = auth_manager.get_authorize_url()
        # print(f"Authorize URL: {auth_url}")
        if (self.sp_oauth.get_cached_token()):
            print("Cached token found")

            try:
                self.sp.recommendations(seed_artists= artist_id)
                print("Success")
            except:
                print("failure")
        else:
            print("no cached token")

    def check_if_follow(self, artists):
        spotify_results = []
        artist_ids = []
        pattern = r'[^A-Za-z0-9 ]'
        artists = filter(None, artists)
        for artist in artists:
            results = self.search_artist(re.sub(pattern, "", artist))
            normalized_name = str(artist).lower().replace(" ","")
            # print(f"{artist} = Hash: {hash(artist)}")
            matching_name = ""
            if not None in results:
                results = filter(None, results)
                for result in results:
                    print(result['name'])
                    normalized_result = str(result['name']).lower().replace(" ","")
                    if (normalized_result == normalized_name):
                        matching_name = result['name']
                        spotify_results.append(artist)
                        artist_ids.append(result['uri'])
                        # if (self.sp.current_user_following_artists(ids= result['id'])):
                        #     print('is following.')
                        # else:
                        #     print('is not following.')
                        break

            # if (matching_name == ""):
            #     target = str(artist)
            #     results = self.search_artist(target)
            #     for result in results:
            #         print(result['name'])
            #         if (result == target):
            #             matching_name = result['name']
            #             spotify_results.append(artist)
            #             break

            print("\n")
        following = []
        not_following = []
        print(spotify_results)
        # print(self.sp.current_user_following_artists(artist_ids))
        return artist_ids

    def get_top_tacks(self, artists):
        for artist in artists:
            print(artist)
            results = self.sp.artist_top_tracks(artist_id= artist)

            for track in results['tracks'][:10]:
                print('track    : ' + track['name'])
                print('uri: ' + track['uri'])
                print()
            print('track    : ' + results['tracks'][0]['name'])
            self.sp.add_to_queue(results['tracks'][0]['uri'])

    def get_now_playing_artist(self):
        result = self.sp.currently_playing()
        artists_names = result['item']['artists']
        artists_names = [artist['name'] for artist in artists_names]

        return artists_names

    def get_now_playing(self):
        result = self.sp.currently_playing()
        artists_names = result['item']['artists']
        artists_names = [artist['name'] for artist in artists_names]
        album_name = result['item']['album']['name']
        song_name = result['item']['name']

        return artists_names, album_name, song_name

### Example result DO NOT DELETE THIS COMMENT! IT HAD TO BE REFORMATTED BY HAND
'''
{
'timestamp': 1735950535949, 
'context': 
	{
	'external_urls': 
		{
		'spotify': 'https://open.spotify.com/collection/tracks'
		},
	'href': 'https://api.spotify.com/v1/me/tracks', 
	'type': 'collection', 
	'uri': 'spotify:user:tdking72:collection'
	}, 
'progress_ms': 136928, 
'item': 
	{
	'album': 
		{
		'album_type': 'album', 
		'artists': [
			{
			'external_urls': 
				{
				'spotify': 'https://open.spotify.com/artist/0lzVrkjlIZJH18hk2Gcjkp'
				}, 
			'href': 'https://api.spotify.com/v1/artists/0lzVrkjlIZJH18hk2Gcjkp', 
			'id': '0lzVrkjlIZJH18hk2Gcjkp', 
			'name': 'Kenji Kawai', 
			'type': 'artist', 
			'uri': 'spotify:artist:0lzVrkjlIZJH18hk2Gcjkp'
			}], 
		'available_markets': ['US'], 
		'external_urls': 
			{
			'spotify': 'https://open.spotify.com/album/4k2ceSwmi8CxgB10rdji7S'
			}, 
		'href': 'https://api.spotify.com/v1/albums/4k2ceSwmi8CxgB10rdji7S', 
		'id': '4k2ceSwmi8CxgB10rdji7S', 
		'images': [
			{
			'height': 640, 
			'url': 'https://i.scdn.co/image/ab67616d0000b27389d3629e8cf641e6fac4d9e9', 
			'width': 640}, 
				{
				'height': 300, 
				'url': 'https://i.scdn.co/image/ab67616d00001e0289d3629e8cf641e6fac4d9e9', 
				'width': 300
				}, 
				{
				'height': 64, 
				'url': 'https://i.scdn.co/image/ab67616d0000485189d3629e8cf641e6fac4d9e9',
				'width': 64
				}], 
			'name': 'Apocalypse World War II - Original Soundtrack', 
			'release_date': '2012-09-06', 
			'release_date_precision': 'day', 
			'total_tracks': 26, 
			'type': 'album', 
			'uri': 
			'spotify:album:4k2ceSwmi8CxgB10rdji7S'
			}, 
		'artists': [
			{
			'external_urls': 
				{
				'spotify': 
				'https://open.spotify.com/artist/0lzVrkjlIZJH18hk2Gcjkp'
				}, 
			'href': 'https://api.spotify.com/v1/artists/0lzVrkjlIZJH18hk2Gcjkp', 
			'id': '0lzVrkjlIZJH18hk2Gcjkp', 
			'name': 'Kenji Kawai', 
			'type': 'artist', 
			'uri': 'spotify:artist:0lzVrkjlIZJH18hk2Gcjkp'
		}], 
		'available_markets': ['US'], 
		'disc_number': 1, 
		'duration_ms': 140506, 
		'explicit': False, 
		'external_ids': 
			{
			'isrc': 'US4R31219025'
			}, 
		'external_urls': 
			{
			'spotify': 'https://open.spotify.com/track/7fKaJIBQgiHRZJdfoMLuXu'
			},
		'href': 'https://api.spotify.com/v1/tracks/7fKaJIBQgiHRZJdfoMLuXu', 
		'id': '7fKaJIBQgiHRZJdfoMLuXu', 
		'is_local': False, 
		'name': 'Shoah', 
		'popularity': 0, 
		'preview_url': None, 
		'track_number': 2, 
		'type': 'track', 
		'uri': 'spotify:track:7fKaJIBQgiHRZJdfoMLuXu'
	}, 
	'currently_playing_type': 'track', 
	'actions': 
		{
		'disallows': 
			{
			'resuming': True
			}}, 
		'is_playing': True
		}
'''

# obj = Spotify_ctrl()
# print(obj.get_followed_artist())
# artist = input("Please enter the name of an artist: ")
# artists = obj.search_artist(artist)
# for i in range(len(artists)):
#     print(f"{i} : {artists[i]['name']}")
#
# artist_selected = int(input("Please select an artist from the list (Enter the corrisponding number): "))
# if int(artist_selected) <= len(artists):
#     # print(artists[artist_selected]['id'])
#     similar_artists = obj.get_similar_artists(artists[artist_selected]['id'])
#     print(similar_artists)

