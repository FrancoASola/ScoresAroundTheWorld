import sys
import scores
import coordinates
import json

def buildgeojson(current_matches):
    current_matches = scores.pullSoccerMatches(current_matches)
    soccer = {"type":"FeatureCollection","features":[]}
    for match_id in current_matches:
        location = current_matches[match_id]['location']
        homeTeam = current_matches[match_id]['Home Team']
        awayTeam = current_matches[match_id]['Away Team']
        score = current_matches[match_id]['score']
        time = current_matches[match_id]['time']
        if not current_matches[match_id].get('coordinates'):
            coords = coordinates.findCoords(location, homeTeam)
            if coords:
                current_matches[match_id]['coordinates'] = [coords['lat'], coords['lng']]
        if current_matches[match_id].get('coordinates'):
            feature = {'type': 'Feature', 'properties': {
                        'Teams:' : [homeTeam, awayTeam],
                        'Score:' : score,
                        'Time:' : time },
                        'geometry' : {
                        'type' : 'Point',
                        'coordinates': current_matches[match_id].get('coordinates')
                        }
            }
            soccer['features'].append(feature)
   
    with open('./static/soccer.geojson', 'w') as geojson:
        json.dump(soccer, geojson)

buildgeojson({})