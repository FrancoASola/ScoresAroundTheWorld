import os
import requests
import json
#from .classes import Match

key = os.environ.get('LIVE_SCORE_KEY')
secret = os.environ.get('LIVE_SCORE_SECRET')
#Pulls Match Data and Correlates with Existing Data
def pullSoccerMatches(current_matches):
    ##TO DO: Need to Encrypt Keys. Find a good way to store current_matchs (Should be inmemory)
    response = requests.get(f"http://livescore-api.com/api-client/scores/live.json?key={key}&secret={secret}")
    if not response:
        return 'No Response from livescore-api'
    data = response.json()
    matches = data['data']['match']
    for match in matches:
        
        match_id = match['id']
        #Add new Matches
        if match_id not in current_matches and match['status'] != 'FINISHED':
            curMatch = Match(match['home_name'],  match['home_id'], match['away_name'], match['score'],  match['time'],  match['location'], match['status'], match['fixture_id']) 
            curMatch.findCoords()
            current_matches[match_id] = curMatch
        #Remove Finished Matches
        elif match_id in current_matches and match['status'] == 'FINISHED':
            ##TO DO:
            #Add finished matches to the finished database. Could have more information regarding game, scores, etc.
            current_matches.pop(match_id)

        #Update Score
        elif match_id in current_matches and match['score'] != current_matches[match_id].score:
            print('need to update score :', current_matches[match_id].homeTeam, current_matches[match_id].score, match.time)
            current_matches[match_id].score = match['score']
            current_matches[match_id].time = match['time']

        #Update Time
        elif match_id in current_matches:
            current_matches[match_id].time = match['time']

    return current_matches if current_matches else 404    

def pullFinishedSoccerMatches(current_matches, date):
    ## TO DO:
    # Store in DB for future use. Redis would work better. 

    url = f"http://livescore-api.com/api-client/scores/history.json?from={date}&to={date}&key={key}&secret={secret}"
    matches = []
    page = 1
    while True:
        response = requests.get(url + f'&page={page}')
        data = response.json()
        if data:
            matches.extend(data['data']['match'])
            if data['data']['next_page']:
                page += 1
            else:
                break  
    for match in matches:
        match_id = match['id']
        #Add new Matches
        if match_id not in current_matches and match['status'] == 'FINISHED':
            curMatch = Match(match['home_name'],  match['home_id'], match['away_name'], match['score'],  match['time'],  match['location'], match['status'], match['fixture_id']) 
            curMatch.findCoords()
            current_matches[match_id] = curMatch   
    
    return current_matches if current_matches else 404            

if __name__ == "__main__":
    print(pullSoccerMatches({}))