from . import scores
import json

def buildgeojson(current_matches, live, date):
    if live:
        current_matches = scores.pullSoccerMatches(current_matches)
    else:
        current_matches = scores.pullFinishedSoccerMatches(current_matches,date)
    soccer = {"type":"FeatureCollection","features":[]}
    for match_id in current_matches:
        match = current_matches[match_id]
        if match.coordinates and match.coordinates != 'N/A':
            feature = {'type': 'Feature', 'properties': {
                        'info' : f"{match.homeTeam} {match.score} {match.awayTeam} <br> Time: {match.time}'",
                        'score': f"{match.score}",
                        'match_id': f"{match_id}"},
                        'geometry' : {
                        'type' : 'Point',
                        'coordinates': [match.coordinates['lng'], match.coordinates['lat']]
                        }
            }
            soccer['features'].append(feature)
    return soccer

    