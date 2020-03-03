import requests
import json

##Find Coordinates Using GeocoderAPI 
def findCoords(location, homeTeam):
    '''Get Coordinates for Stadium'''
    if location:
        loc = location.replace(' ', '+')
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={loc}&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
        coords = json.loads(response.text)
        if coords['results']:
            return coords['results'][0]['geometry']['location']
    if homeTeam:
        home_team = homeTeam.replace(' ', '+')
        home_team += '+stadium'
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={home_team}&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
        coords = json.loads(response.text)
        if coords['results']:
            return coords['results'][0]['geometry']['location']

