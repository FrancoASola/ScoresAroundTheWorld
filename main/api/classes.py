import pymongo
import requests
import json
from main.extensions import mongo
import datetime

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
        ins = {'_id': self.homeTeamID, 'coordinates': 'N/A'}
        mongo.db.coordinates.insert_one(ins)
        self.coordinates = 'N/A'
        return 
        
                
class Message:

    def __init__(self, match_id, user, text):
        self.match_id = match_id
        self.user = user
        self.text = text
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.date = datetime.date.today().strftime("%m/%d/%y")


class Messages:

    def __init__(self, match_id):
        self.match_id = match_id
        self.message_collection = mongo.db.messages

    def postMessage(self, message):
        '''check if message exist and update or insert accordingly'''
        self.message_collection.update_one({'_id': self.match_id}, {'$push': {'messages': [message.__dict__]}}, upsert=True)

    def getMessages(self):
        messages = self.message_collection.find_one({'_id': self.match_id})
        return messages if messages else 'No Messages'

class Highlight:
    
    def __init__(self, match_id, user, url, title):
        self.match_id =match_id
        self.user = user
        self.url = url
        self.title = title
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.date = datetime.date.today().strftime("%m/%d/%y")

class Highlights:

    def __init__(self, match_id):
        self.match_id = match_id
        self.highlight_collection = mongo.db.Highlights
    
    def postHighlight(self, message):
        '''#check if message exist and update or insert accordingly:'''
        self.highlight_collection.update_one({'_id': self.match_id}, {'$push': {'messages': [message.__dict__]}}, upsert=True)

    def getHighlights(self):
        highlights = self.highlight_collection.find_one({'_id': self.match_id})
        return highlights if highlights else 'No Highlights'