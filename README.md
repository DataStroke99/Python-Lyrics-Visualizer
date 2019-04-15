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










