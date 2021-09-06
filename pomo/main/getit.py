import requests
import json



def fetch(title,year):
    url = f'http://www.omdbapi.com/?t={title}&y={year}&apikey=934ea8b2'

    r = requests.get(url=url)

    print(r.json()['Year'])


fetch('friends','')