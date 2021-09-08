import requests
import json

from requests.models import default_hooks



def fetch(title):
    url = f'http://www.omdbapi.com/?s={title}&apikey=934ea8b2'

    r = requests.get(url=url)
    titles = []
    year = []
    imdb_id = []
    type = []
    poster_link = []


    r = requests.get(url=url)

    res = r.json()['Response']

    if res=="False":
        return({},0,False)


    for i in r.json()['Search']:

        titles.append(i['Title'])
        year.append(i['Year'])
        imdb_id.append(i['imdbID'])
        type.append(i['Type'])
        poster_link.append(i['Poster'])

        n = int(r.json()['totalResults'])


    d = {
            'title':titles,
            'year':year,
            'poster_link':poster_link,
            'type':type,
            'imdb_id':imdb_id,

        }


    return(d,n,True)
    
