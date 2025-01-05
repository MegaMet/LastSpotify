import statistics
import datetime
from flask import Flask, render_template


import pandas as pd
from spotify_ctrl import Spotify_ctrl
from lastfm_ctrl import Lastfm_ctrl

# input("Please enter the name of an artist: ")
# input("How many similar artist are you looking for?: ")
# input("Do you wish to ignore similar artist already recommended by Spotify?: ")
# input("Do you wish to ignore similar artist you already have liked?: ")
# input("Would you like t6 go down the rabbit hole? (Adding a song to your 'likes' wil start a new search with this artist and ignore the artists you previously listened to, potentially introducing new artist.)")

lfm = Lastfm_ctrl()
sp = Spotify_ctrl()
# def lastfm_get_similar_artist():
app = Flask(__name__)

@app.route("/")
def home():
    current_Year = datetime.datetime.now().year
    artists, album, song = sp.get_now_playing()
    return render_template('index.html', artists= artists, album= album, song= song, year= current_Year)

@app.route("/test/<variable1>/<int:variable2>")
def test(variable1, variable2):
    return (f"Variable 1: {variable1} || Variable 2: {variable2}")

def get_similar_artist(artist_name):
    lastFm_similar_artist = lfm.get_similar_artists(artist_name)
    print(len(lastFm_similar_artist))

    likeness = int(input("Please enter level of deviation (10 :most - 1 : least): "))
    if (likeness == 0):
        print("Limiting selection to first 3 resutls")
        lastFm_similar_artist = lastFm_similar_artist[0:3]
    elif (likeness < 1 or likeness > 10):
        print("Level enter is outside the range")
        exit()
    else:
        match likeness:
            case 10:
                lastFm_similar_artist = lastFm_similar_artist[0:25]
            case 9:
                lastFm_similar_artist = lastFm_similar_artist[25:50]
            case 8:
                lastFm_similar_artist = lastFm_similar_artist[50:75]
            case 7:
                lastFm_similar_artist = lastFm_similar_artist[75:100]
            case 6:
                lastFm_similar_artist = lastFm_similar_artist[100:123]
            case 5:
                lastFm_similar_artist = lastFm_similar_artist[125:150]
            case 4:
                lastFm_similar_artist = lastFm_similar_artist[150:175]
            case 3:
                lastFm_similar_artist = lastFm_similar_artist[175:200]
            case 2:
                lastFm_similar_artist = lastFm_similar_artist[200:225]
            case 1:
                lastFm_similar_artist = lastFm_similar_artist[225:250]

    artist_list = [artist['name'] for artist in lastFm_similar_artist]
    average_similarity_score = statistics.mean([float(artist['match']) for artist in lastFm_similar_artist])
    # print(artist_list)
    spotify_similar_artist = sp.check_if_follow(artist_list)
    print(average_similarity_score)

    sp.get_top_tacks(spotify_similar_artist)

def start():
    artist = input("Please enter the name of an artist: ")
    if (artist == "sp_search"):
        print("Spotify restricted artist search enabled")
        artist = input("Please enter the name of an artist: ")
        print(f"hash of input: {artist} = {hash(artist)}")
        normalized_name = str(artist).lower().replace(" ", "")
        normalized_name_hash = hash(normalized_name)
        artist_options = sp.search_artist(artist, limit= 20)
        for i in range(len(artist_options)):
            print(f"{i} : {artist_options[i]['name']}")
            normalized_result = str(artist_options[i]['name']).lower().replace(" ", "")
            normalized_result_hash = hash(normalized_result)
            print(f"{normalized_result} = hash: {normalized_result_hash} \n{normalized_name} = hash: {normalized_name_hash}")

    elif (artist == "sp_nowplaying"):
        artist_options = sp.get_now_playing_artist()
        if (len(artist_options) > 1):
            for i in range(len(artist_options)):
                print(f"{i} : {artist_options[i]}")

            artist_selected = int(input("Please select an artist from the list (Enter the corrisponding number): "))
            if int(artist_selected) <= len(artist_options):
                artist_selected = artist_options[artist_selected]
                print(artist_selected)
        else:
            artist_selected = artist_options
            print(artist_selected)

        get_similar_artist(artist_selected)

    else:
        print("Now searching Last.fm")
        artist_options = lfm.search_artist(artist= artist)
        for i in range(len(artist_options)):
            print(f"{i} : {artist_options[i]['name']}")

        artist_selected = int(input("Please select an artist from the list (Enter the corrisponding number): "))
        if int(artist_selected) <= len(artist_options):
            artist_selected = artist_options[artist_selected]
            print(artist_selected)

        get_similar_artist(artist_selected['name'])


if (__name__ == "__main__"):
    app.run(debug= True)