import re
import nltk
import json
import flask
from Gui import *
from nltk import *
import pandas as pd
import seaborn as sns
from nltk.corpus import *
from textblob import TextBlob
from nltk import word_tokenize
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from bs4 import BeautifulSoup as bs
from nltk.corpus import wordnet as wn
from wordcloud import wordcloud,WordCloud,STOPWORDS
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
from termcolor import colored
import requests
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import sys
from nltk.tokenize import RegexpTokenizer
from rhyme_detect import *


# API
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
client_token = 'CLIENT_TOKEN'


# basic variables
orig_url = 'https://genius.com'
base_url = 'https://api.genius.com'
path = 'search/'
search = '/search?q='
header = {'Authorization':'Bearer '+client_token}
pattern =  '(?m)^\[.*\n?'
corpus_root = ''
file  ='song.txt'

song_list = []
album_list=[]
sort_type=[]
ssid=[]

def image_fetch(artist,song_api,k):
    try:
        song_url = base_url+song_api
        response = requests.get(song_url,headers=header)
        json = response.json()
        path = json['response']['song']['song_art_image_url']
        artist =artist
        k=str(k)
        img_name = artist+k+'.jpg'
        file_path = 'static/images/'
        f = open(file_path+img_name,'wb')
        f.write(requests.get(path).content)
        f.close()

        #page = requests.get(page_url)
        return path
    except:
        print('error')



def get_album(song_api):
    try:
        song_url = base_url+song_api
        response = requests.get(song_url,headers=header)
        data = response.json()
        page_url = data['response']['song']['album']['url']
        page =   requests.get(page_url)

        #print(page_url)
        html  = bs(page.text,"html.parser")

        #[h.extract() for h in html('script')]

        lyrics = html.findAll('h3', class_='chart_row-content-title')
        #print(lyrics.get_text())
        for i in lyrics:
            lyr = i.get_text().split()
            lyr.remove('Lyrics')
            l = ' '.join(lyr)
           # print(l)



        img = html.findAll('img', class_='cover_art-image')
        #for i in img:
           # print(i['src'])

        #print(img)


        return img
    except:
        print('error')




def lyrics_fetch(song_api):
    try:
        song_url = base_url+song_api
        response = requests.get(song_url,headers=header)
        data = response.json()
        path = data['response']['song']['path']
        page_url = orig_url+path
        page = requests.get(page_url)

        path2 = data['response']['song']['album']['url']
       # print(path2)

        parsed = json.dumps(response.json(), indent=4)
        #print(parsed)

        #print(page_url)
        html  = bs(page.text,"html.parser")
        [h.extract() for h in html('script')]
        lyrics = html.find('div', class_='lyrics')


        song = html.find('h1')
        song =  song.get_text()
        name = html.find('h2')
        name = name.get_text()
        feat = html.find('h3')
        feat =  feat.get_text()
        details = song + name  + feat
        song_list.append(song)
        lyrics = details+ lyrics.get_text()
        #lyrics = lyrics.get_text()
        return lyrics
    except:
        print('error')



def get_lyrics(artist,num):
    try:
        artist_id = ''
        search_url = base_url + "/search?q=" + artist
        response = requests.get(search_url, headers=header)
        json = response.json()
        num_songs = num #input('Number of songs: ')
        for hit in json['response']['hits']:
            if hit['result']['primary_artist']['name'] == artist:
                artist_id = hit['result']['primary_artist']['api_path']
                break
        artist_url = base_url + artist_id + '/songs?sort=popularity&per_page=%s' % num_songs
        #artist_url = base_url + artist_id + '/songs?sort=title&per_page=%s' % num_songs
        #artist_url = base_url + artist_id + '/songs?sort=release_date&per_page=%s' % num_songs
        #print(artist_url)
        artist_response = requests.get(artist_url, headers=header)
        artist_json = artist_response.json()
        song_paths = {}
        song_lyrics = {}
        i = 0
        k=0
        lyrics_p = []
        lyrics =[]
        for song in artist_json['response']['songs']:
            song_paths[song['title_with_featured']] = song['api_path']
            if i < int(num_songs):
                lyrics_p.append( song['api_path'])
                i = i +  1
        for song,song_path in song_paths.items():
            #song_lyrics[song] = lyrics_fetch(song_path)
            lyrics.append(lyrics_fetch(song_path))

            img = image_fetch(artist,song_path,k)
           # print(img)
            get_album(song_path)
            k+=1
        return lyrics
    except:
        print('error')




def _get(path, params=None, headers=None):

    # generate request URL
    requrl = '/'.join([base_url, path])
    token = "Bearer {}".format(client_token)
    if headers:
        headers['Authorization'] = token
    else:
        headers = {"Authorization": token}

    response = requests.get(url=requrl, params=params, headers=headers)
    response.raise_for_status()

    return response.json()







def get_artist_songs(artist_id):
    # initialize variables & a list.
    current_page = 1
    next_page = True
    songs = []

    # main loop
    while next_page:

        path = "artists/{}/songs/".format(artist_id)
        params = {'page': current_page}
        data = _get(path=path, params=params)

        page_songs = data['response']['songs']

        if page_songs:
            # add all the songs of current page,
            # and increment current_page value for next loop.
            songs += page_songs
            current_page += 1
        else:
            # if page_songs is empty, quit.
            next_page = False

    # get all the song ids, excluding not-primary-artist songs.
    songs = [song["id"] for song in songs
             if song["primary_artist"]["id"] == artist_id]
    print(songs)

    return songs





def get_song_information(song_ids):
    # initialize a dictionary.
    song_list = {}

    # main loop
    for i, song_id in enumerate(song_ids):
        #print("id:" + str(song_id) + " start. ->")

        path = "songs/{}".format(song_id)
        data = _get(path=path)["response"]["song"]
        #print(data)

        song_list.update({
        i: {
            "title": data["title"],
            "album": data["album"]["name"] if data["album"] else "<single>",
            "release_date": data["release_date"] if data["release_date"] else "unidentified",
            "featured_artists":
                [feat["name"] if data["featured_artists"] else "" for feat in data["featured_artists"]],
            "producer_artists":
                [feat["name"] if data["producer_artists"] else "" for feat in data["producer_artists"]],
            "writer_artists":
                [feat["name"] if data["writer_artists"] else "" for feat in data["writer_artists"]],
            "genius_track_id": song_id,
            "genius_album_id": data["album"]["id"] if data["album"] else "none"}
        })
        #print(song_list)
        #print("-> id:" + str(song_id) + " is finished. \n")
        if song_list[i]['album'] == 'The Slim Shady LP':
            print(song_list[i]['title'] + str(song_id))
            ssid.append(song_id)
    return song_list





# find artist id from given data.
find_id = _get("search", {'q': artist})
for hit in find_id["response"]["hits"]:
   if hit["result"]["primary_artist"]["name"] == artist:
       artist_id = hit["result"]["primary_artist"]["id"]

       break





num = 2
lines = []
artist = 'Eminem'


lines = get_lyrics(artist,num)
conv = convrt_lines(lines)


print(artist_id)
info=[]
song_ids = get_artist_songs(artist_id)
info = get_song_information(song_ids)

print(info)





'''text = open('song.txt')
plt.figure(figsize=(20,20))
wc = WordCloud(height=300, width=500, background_color='white',max_words=10000, stopwords=STOPWORDS, max_font_size=50)
wc.generate(' '.join(text))
plt.imshow(wc.recolor(colormap='RdBu'),interpolation='bilinear')
plt.title("Power")
plt.axis('off')
#plt.show()'''






def figure(lines):

    numb_word=0
    df = pd.DataFrame(columns=('Songs','Words','Lyrics'))

    for sent in range(0,len(song_list)):
        numb_word = len(lines[sent].split())
        df.loc[sent] = (song_list[sent], numb_word,lines[sent])
        # text = open('song.txt')
        plt.figure(figsize=(16, 9))
        wc = WordCloud(height=300, width=500, background_color='white', max_words=10000, stopwords=STOPWORDS,
                       max_font_size=50)
       # wc.generate('\n'.join(lines[sent]))
        wc.generate(lines[sent])
        plt.imshow(wc.recolor(colormap='RdBu'), interpolation='bilinear')
        plt.title(song_list[sent])

        plt.axis('off')
       # plt.show()

    print(colored(df.head(),'green'))
    df.plot.bar(x='Songs', y='Words', title='Number of Words for each Song by'+artist)
   # plt.show()

