import pymongo
import requests
import json
from main.extensions import mongo

class Match:

    def __init__(self, homeTeam, homeTeamID, awayTeam, score, time, location, status, fixtureID):
        self.homeTeam = homeTeam
        self.homeTeamID = homeTeamID
        self.awayTeam = awayTeam
        self.score = score
        self.time = time
        self.location = location
        self.status = status
        self.fixtureID = fixtureID
        self.coordinates = None

    #Check if Home Team is on DB if not, call on Google Geocoding API. TO DO: change
    def findCoords(self):
        '''Get Coordinates for Stadium'''
        coords = mongo.db.coordinates.find_one({'_id': self.homeTeamID})
        if coords:
            if coords['coordinates']:
                self.coordinates = coords['coordinates']
            else:
                mongo.db.coordinates.update_one({'_id' : self.homeTeamID}, {'$set': {'coordinates': 'N/A'}})
                self.coordinates = 'N/A'                
            return 
        if self.location:
            loc = self.location.replace(' ', '+')
            response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={loc}&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
            coords = json.loads(response.text)
            if coords['results']:
                ins = {'_id': self.homeTeamID, 'coordinates': coords['results'][0]['geometry']['location']}
                mongo.db.coordinates.insert_one(ins)
                self.coordinates = coords['results'][0]['geometry']['location']
                return 
        if self.homeTeam:
            home_team = self.homeTeam.replace(' ', '+')
            home_team += '+stadium'
            response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={home_team}&key=AIzaSyCMjW8GePLfbExz9gO-zD-3f6IkaUhXSxo')
            coords = json.loads(response.text)
            if coords['results']:
                ins = {'_id': self.homeTeamID, 'coordinates': coords['results'][0]['geometry']['location']}
                mongo.db.coordinates.insert_one(ins)
                self.coordinates = coords['results'][0]['geometry']['location']
                return 
            else: 
                ins = {'_id': self.homeTeamID, 'coordinates': 'N/A'}
                mongo.db.coordinates.insert_one(ins)
                self.coordinates = 'N/A'
                return 
                




