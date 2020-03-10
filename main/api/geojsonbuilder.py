from . import scores
import json

def buildgeojson(current_matches):
    current_matches = scores.pullSoccerMatches(current_matches)
    soccer = {"type":"FeatureCollection","features":[]}
    for match_id in current_matches:
        match = current_matches[match_id]
        if match.coordinates and match.coordinates != 'N/A':
            feature = {'type': 'Feature', 'properties': {
                        'info' : f"{match.homeTeam} {match.score} {match.awayTeam} \n Time: {match.time}'",
                        'score': f"{match.score}"},
                        'geometry' : {
                        'type' : 'Point',
                        'coordinates': [match.coordinates['lng'], match.coordinates['lat']]
                        }
            }
            soccer['features'].append(feature)
    return soccer
if __name__ == "__main__":
    buildgeojson({})
    