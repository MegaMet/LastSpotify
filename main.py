
"""
Bug List
=====================
-The deviation value is not being applied to the query when the search is performed
(example url: http://127.0.0.1:5000/<page>>/<artist>>/<deviation>>)
(example url: http://127.0.0.1:5000/search/Lems/10)

-when a query is made where the similar artist results is 0, returns a NONE result and an error screen

"""



import math
import statistics
import datetime

import requests
from flask import Flask, render_template, request, redirect, url_for


import pandas as pd
from spotify_ctrl import Spotify_ctrl
from lastfm_ctrl import Lastfm_ctrl

lfm = Lastfm_ctrl()
sp = Spotify_ctrl()
# def lastfm_get_similar_artist():
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def home(path=None):
    # current_Year = datetime.datetime.now().year
    # artists, album, song = sp.get_now_playing()
    # return render_template('index.html', artists= artists, album= album, song= song, year= current_Year)

    if request.method == "POST":
        # Perform search and return results
        artist = request.form['search']
        deviation = request.form['deviation']

        return redirect(url_for("search_artist", artist=artist, deviation=deviation))

    return render_template('index.html')

@app.route("/test/<variable1>/<int:variable2>")
def test(variable1, variable2):
    return (f"Variable 1: {variable1} || Variable 2: {variable2}")

@app.route('/results/<string:artist_name>/<int:likeness>')
def get_similar_artist(artist_name, likeness):
    lastFm_similar_artist = lfm.get_similar_artists(artist_name)
    print(lastFm_similar_artist)

    if (likeness == 0):
        print("Limiting selection to first 3 resutls")
        lastFm_similar_artist = lastFm_similar_artist[0:3]
    elif (likeness < 1 or likeness > 10):
        print("Level enter is outside the range")
        exit()
    else:
        total_count = len(lastFm_similar_artist)
        division = 20
        intervals = math.floor(total_count / division)
        min = intervals * (likeness - 1)
        max = intervals * likeness
        print(f'{min} : {max}')
        lastFm_similar_artist = lastFm_similar_artist[min:max]


    artist_list = [artist['name'] for artist in lastFm_similar_artist]
    average_similarity_score = statistics.mean([float(artist['match']) for artist in lastFm_similar_artist])
    spotify_similar_artist = sp.find_aritst(artist_list)
    spotify_similar_artist_ids = [artist['uri'] for artist in spotify_similar_artist]
    print(average_similarity_score)

    sp.get_top_tacks(spotify_similar_artist_ids)
    return render_template("index.html", page="results", artist_results=spotify_similar_artist)

@app.route('/search/<string:artist>/<int:deviation>')
def search_artist(artist, deviation):


    print("Now searching Last.fm")
    artist_options = lfm.search_artist(artist=artist)

    # print(artist_options)
    # return artist_options
    return render_template("index.html", page="search", searched_artist=artist, artist_options=artist_options, likeness=deviation)



# Take the value in the search box and pass it through this fuction
# @app.route('/search/<string:artist>')
@app.route('/search_debug/<string:artist>/<int:likeness>')
def search_artist_debug(artist):
    if (artist == ""):
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
        searched_artist = ""
        if request.method == "POST":
            searched_artist = request.form.get("artist")

        print("Now searching Last.fm")
        artist_options = lfm.search_artist(artist= artist)

        # print(artist_options)
        # return artist_options
        return render_template("index.html", page= "search", artist_options= artist_options)


# REVIVE ME!!!
# -------------------
# @app.route('/results/<string:artist_selected>/<int:likeness>')
def search_artist_select_results(artist_selected, likeness):
    # artist_selected = int(input("Please select an artist from the list (Enter the corrisponding number): "))
    # if int(artist_selected) <= len(artist_options):
    #     artist_selected = artist_options[artist_selected]
    #     print(artist_selected)


    get_similar_artist(artist_selected, likeness)
# -------------------


# artist = input("Please enter the name of an artist: ")
# artist_options = search_artist(artist)
#
# for i in range(len(artist_options)):
#     print(f"{i} : {artist_options[i]['name']}")
#
# artist_selected = int(input("Please select an artist from the list (Enter the corrisponding number): "))
# likeness = int(input("Please enter the level of deviation you are looking for (Enter 1 minimum - 20 maximum): "))
#
# search_artist_select_results(artist_options, artist_selected, likeness)

if (__name__ == "__main__"):
    app.run(debug= True)