import scores
import coordinates
import json

def buildgeojson(current_matches):
    current_matches = scores.pullSoccerMatches(current_matches)
    for match in current_matches:
        coords = coordinates.findCoords(match['location'])
        match['coordinates'] = [coords['lat'], coords['lng']]

        print(match)

print(buildgeojson({}))