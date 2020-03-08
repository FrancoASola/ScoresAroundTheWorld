import requests
import json

#Pulls Match Data and Correlates with Existing Data
def pullSoccerMatches(current_matches):
    ##TO DO: Need to Encrypt Keys. Find a good way to store current_matchs (Should be inmemory)
    key = 'dovU4iInbWpHnIHs'
    secret = '0kKYErWnwnA61f1eDw9IOR50OvHbdpEd'
    response = requests.get(f"http://livescore-api.com/api-client/scores/live.json?key={key}&secret={secret}")
    data = response.json()
    matches = data['data']['match']
    for match in matches:
        match_id = match['id']
        #Add new Matches
        if match_id not in current_matches and (match['status'] != 'FINISHED' or match['status'] != 'NOT STARTED'):
            current_matches[match_id] = {'Home Team': match['home_name'],
                                         'Home Team ID': match['home_id'],
                                            'Away Team': match['away_name'],
                                            'score': match['score'],                           
                                            'time': match['time'],
                                            'location' : match['location'],
                                            'status' : match['status'],
                                            'fixture_id': match['fixture_id']}
        #Remove Finished Matches
        if match_id in current_matches and match['status'] == 'FINISHED':
            ##TO DO:
            #Add finished matches to the finished database. Could have more information regarding game, scores, etc.
            current_matches.pop(match_id)

        #Update Score
        elif match_id in current_matches and match['score'] != current_matches[match_id]['score']:
            print('need to update score :', current_matches[match_id]['Home Team'], current_matches[match_id]['score'], match['score'])
            current_matches[match_id]['score'] = match['score']
            current_matches[match_id]['time'] = match['time']

        #Update Time
        elif match_id in current_matches:
            current_matches[match_id]['time'] = match['time']

    return current_matches

if __name__ == "__main__":
    print(pullSoccerMatches({}))