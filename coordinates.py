import requests
import json

##Find Coordinates Using GeocoderAPI 
def findCoords(location):
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=Estadio+Eva+Per�n+de+Jun�n&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
    coords = json.loads(response.text)
    return coords['results'][0]['geometry']['location']
