import re
import nltk
import json
import flask
from Gui import *
from nltk import *
import pandas as pd
import seaborn as sns
from Flask_web import *
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



from prep_functions import *


# API
client_id = ''
client_secret = ''
client_token = ''


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



def start(artist,num):
    artist = artist
    num = num
    lines = []
    lines = get_lyrics(artist,num)
    #lines = '\n'.join(lines)
    #print(lines)
    return lines

def convrt_lines(lines):
    l = []
    word  =[]
    full=[]
    numb=0
    f=[]
    for sent in range(0, len(song_list)):
        for lyr in lines[sent].split('\n'):
            if lyr =='':
                continue
            else:
             word.append(lyr)
             f = word.copy()
             #full.append(word[0])
             full.insert(numb,f)
             word.pop()
             numb+=1
        l.append(full)
        full=[]
        word=[]
        numb=0

    return l


#for sent in range(0, len(song_list)):
   # for i in conv[sent]:
       # print(i)



num = 2
lines = []
artist = 'Pusha-T'

lines = get_lyrics(artist,num)
display_lines =[]
display_lines = lines.copy()

conv = convrt_lines(lines)

s=1
for i in conv:
    for each_line in i:
        for linee in each_line:


                lw = last_word(linee)
                print(lw)


                if s>=len(i):
                    s=0
                ls = ''.join(i[s])


                lw2 = last_word(ls)
                print(lw2)
                print(word_similarity(lw,lw2))

                s += 1


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


















































#pd.set_option('display.max_colwidth', -1)
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)


#df = pd.DataFrame(conv)
#print(df)


#print(format_sent(lines))
#figure(lines)




'''def format_sent(sent):
    for i in sent:
        #maybe clear the punctuations like '[]' and stuff
        return({word: True for word in nltk.word_tokenize(i)})


def format_sentence(sent):
    return({word: True for word in nltk.word_tokenize(sent)})

pos = []
with open("text/pos_tweets.txt") as f:
    for i in f:
        pos.append([format_sentence(i), 'pos'])

neg = []
with open("text/neg_tweets.txt") as f:
    for i in f:
        neg.append([format_sentence(i), 'neg'])

training = pos[:int((.8)*len(pos))] + neg[:int((.8)*len(neg))]
test = pos[int((.8)*len(pos)):] + neg[int((.8)*len(neg)):]

classifier = NaiveBayesClassifier.train(training)
#classifier.show_most_informative_features()


for sent in range(0, len(song_list)):
    for i in conv[sent]:
        print(i)
        print(classifier.classify(format_sent(i)))
        

#print(classifier.classify(format_sent(lines)))

#print(accuracy(classifier, test))'''






#c = clear_cluter(lines)
#print(c)
#t = tokenize(lines)
#print(t)




sys.exit('')





