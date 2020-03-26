from pymongo import MongoClient

client = MongoClient('mongodb+srv://Franco:SK81sc00@cluster0-3mgy4.gcp.mongodb.net/ScoresAroundWorld?retryWrites=true&w=majority')

db = client.ScoresAroundWorld
collection = db.coordinates

print(collection.find_one({'name': 'test'}))