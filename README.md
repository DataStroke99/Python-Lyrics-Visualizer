# RapRhymeDetector
A Python program which detects rhymes


# Getting Data
I get the lyrics and all of the data from API offered by genius.com, which is a great website which has music data and lyrics easily avaliable. so i applied for the api and started accessing it. 
I found that another creator has made a python binding of the api so its convinent to use his version but i decided that i wanted to have a custom one as i would be experimenting with it a lot. if you want to see the binding check lyrical genius.

Using Genius. API

Once you register for the api the user will get 3 client keys, 

    client_id = 'CLIENT_ID'
    client_secret = 'CLIENT_SECRET'
    client_token = 'CLIENT_TOKEN'

    orig_url = 'https://genius.com'
    base_url = 'https://api.genius.com'
    path     = 'search/'
    search   = '/search?q='
    header   = {'Authorization':'Bearer '+ client_token}
  Helpful projects like - https://github.com/dlarsen5/PyRap/blob/master/Retrieve_Lyrics.py
  and few . more helped me to form the basis of my project.
  
 # Fetching Data
 There are 2 main functions whihc deal with the genius.com api and its resulting JSON data. properly nagviating it to get the appropriate information. in this section 
 
     def lyrics_fetch(song_api):
        try:
            song_url = base_url+song_api
            response = requests.get(song_url,headers=header,verify=False)
            json = response.json()
            path = json['response']['song']['path']
            page_url = orig_url+path
            page = requests.get(page_url)
            #print(json)
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
            response = requests.get(search_url, headers=header, verify=False)
            json = response.json()
            num_songs = num #input('Number of songs: ')
            for hit in json['response']['hits']:
                if hit['result']['primary_artist']['name'] == artist:
                    artist_id = hit['result']['primary_artist']['api_path']
                    break
            artist_url = base_url + artist_id + '/songs?sort=popularity&per_page=%s' % num_songs
            artist_response = requests.get(artist_url, headers=header)
            artist_json = artist_response.json()
            song_paths = {}
            song_lyrics = {}
            i = 0
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
            return lyrics
        except:
            print('error')










