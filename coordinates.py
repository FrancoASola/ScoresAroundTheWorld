import requests
import json

##Find Coordinates Using GeocoderAPI 
def findCoords(location):
    loc = location.replace(' ', '+')
    response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={loc}&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
    coords = json.loads(response.text)
    return coords['results'][0]['geometry']['location']
