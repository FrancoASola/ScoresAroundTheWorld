import sys
import scores
import json
import coordinates

def buildgeojson(current_matches):
    current_matches = scores.pullSoccerMatches(current_matches)
    soccer = {"type":"FeatureCollection","features":[]}
    for match_id in current_matches:
        match = current_matches[match_id]
        location = match['location']
        homeTeam = match['Home Team']
        TeamID = match['Home Team ID']
        awayTeam = match['Away Team']
        score = match['score']
        time = match['time']
        if not match.get('coordinates'):
            coords = coordinates.findCoords(location, homeTeam, TeamID)
            if coords == 'N/A':
                match['coordinates'] = 'N/A'
            elif coords:
                match['coordinates'] = [coords['lng'], coords['lat']]
        if match.get('coordinates') != None and match.get('coordinates') != 'N/A':
            feature = {'type': 'Feature', 'properties': {
                        'info' : f"{homeTeam} {score} {awayTeam} \n Time: {time}'",
                        'score': f"{score}"},
                        'geometry' : {
                        'type' : 'Point',
                        'coordinates': match.get('coordinates')
                        }
            }
            soccer['features'].append(feature)
    with open('./static/soccer.geojson', 'w') as geojson:
        json.dump(soccer, geojson)

if __name__ == "__main__":
    buildgeojson({})
    