import requests
import json

#Pulls Match Data and Correlates with Existing Data
def pullSoccerMatches(current_matches):
    ##TO DO: Need to Encrypt Keys. Find a good way to store current_matchs (Should be inmemory)
    key = 'dovU4iInbWpHnIHs'
    secret = '0kKYErWnwnA61f1eDw9IOR50OvHbdpEd'
    response = requests.get(f"http://livescore-api.com/api-client/scores/live.json?key={key}&secret={secret}")
    data = json.loads(response.text)
    matches = data['data']['match']
    for match in matches:
        match_id = match['id']
        if match_id not in current_matches and (match['status'] == 'IN PLAY' or match['status'] == 'FINISHED'):
            current_matches[match_id] = {'Home Team': match['home_name'],
                                            'Away Team': match['away_name'],
                                            'score': match['score'],                           
                                            'time': match['time'],
                                            'location' : match['location'],
                                            'status' : match['status'],
                                            'fixture_id': match['fixture_id']}
        elif match_id in current_matches and match['score'] != current_matches[match_id]['score']:
            print('need to upgrade score')
    
    return current_matches
