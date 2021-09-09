import requests
import json

from requests.models import default_hooks



def fetch(id):
    url = f'http://www.omdbapi.com/?i={id}&apikey=934ea8b2'

    r = requests.get(url=url)

    d = {
            'title':r.json()['Title'],
            'genre':r.json()['Genre'], 
            'year':r.json()['Year'],
            'released':r.json()['Released'],
            'runtime':r.json()['Runtime'],
            'cast':r.json()['Actors'],
            'plot':r.json()['Plot'],
            'country':r.json()['Country'],
            'poster_link':r.json()['Poster'],
            'metascore':r.json()['Metascore'],
            'imdbRating':r.json()['imdbRating'],
            'type':r.json()['Type'],
            'imdb_id':r.json()['imdbID'],

        }

    return(d)
    
