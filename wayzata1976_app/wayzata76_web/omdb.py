import os
import requests
import json


data_endpoint = f'http://www.omdbapi.com/?apikey={os.getenv("OMDB_API_KEY")}&'
poster_endpoint = f'http://img.omdbapi.com/?apikey={os.getenv("OMDB_API_KEY")}&'

def get_title(title:str, year=1976) -> dict:
    response = requests.get(data_endpoint+f't={title}&y={year}')
    title_data = json.loads(response)
    return title_data

def poster(title_data):
    url = title_data['Poster']
    poster = requests.get(url)
    return poster

def awards(title_data):
    award_data = title_data['Awards']
    return award_data

def box_office(title_data):
    box_office = title_data['BoxOffice']
    return box_office

def ratings(title_data) -> [dict]:
    ratings = title_data['Ratings']

def actors(title_data):
    actors = title_data['Actors']
    return 

def released(title_data):
    date = title_data['Released']
    return date

def plot(title_data):
    plot = title_data['Plot']
    return plot

def director(title_data):
    director = title_data['Director']
    return director