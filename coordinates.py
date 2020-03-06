import requests
import json
import pymongo

##TO DO:
#Secure PW
client = pymongo.MongoClient("mongodb+srv://Franco:SK81sc00@cluster0-3mgy4.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.ScoresAroundWorld
collection = db.coordinates

##Find Coordinates Using GeocoderAPI 
def findCoords(location, homeTeam, TeamID):
    '''Get Coordinates for Stadium'''
    coords = collection.find_one({'_id': TeamID})
    if coords:
        return coords['coordinates']
    if location:
        loc = location.replace(' ', '+')
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={loc}&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
        coords = json.loads(response.text)
        if coords['results']:
            ins = {'_id': TeamID, 'coordinates': coords['results'][0]['geometry']['location']}
            collection.insert_one(ins)
            return coords['results'][0]['geometry']['location']
    if homeTeam:
        home_team = homeTeam.replace(' ', '+')
        home_team += '+stadium'
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={home_team}&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
        coords = json.loads(response.text)
        if coords['results']:
            ins = {'_id': TeamID, 'coordinates': coords['results'][0]['geometry']['location']}
            collection.insert_one(ins)
            return coords['results'][0]['geometry']['location']
        else: 
            ins = {'_id': TeamID, 'coordinates': None}
            collection.insert_one(ins)
