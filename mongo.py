import pymongo
client = pymongo.MongoClient("mongodb+srv://Franco:SK81sc00@cluster0-3mgy4.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.ScoresAroundWorld
collection = db.coordinates

post1 = {'_id': 5, 'name': 'joe', 'score': 5}
post2 = {'_id': 6, 'name': 'bill', 'score': 35}

#results = collection.update_one({'_id': 5}, {'$add': {'message':"'sup?"}})
collection.insert_many([post1, post2])