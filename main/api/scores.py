import os
import requests
import json
from .classes import Match

key = os.environ.get('LIVE_SCORE_KEY')
secret = os.environ.get('LIVE_SCORE_SECRET')

#Pulls Match Data and Correlates with Existing Data
def pullSoccerMatches(current_matches):

    try:
        response = requests.get(f"http://livescore-api.com/api-client/scores/live.json?key={key}&secret={secret}")
    except:
        return 'No Response from Live Score'

    data = response.json()
    matches = data['data']['match']
    current_matches = buildCurrentMatches(matches, current_matches)

    return current_matches if current_matches else 404    

def pullFinishedSoccerMatches(date):

    url = f"http://livescore-api.com/api-client/scores/history.json?from={date}&to={date}&key={key}&secret={secret}"
    matches = []
    page = 1
    while True:
        try:
            response = requests.get(url + f'&page={page}')
        except:
            return 'No Response from Live Score'
        data = response.json()
        if data:
            matches.extend(data['data']['match'])
            if data['data']['next_page']:
                page += 1
            else:
                break  

    finished_matches = buildFinishedMatches(matches)
    
    return finished_matches if finished_matches else 404            

def buildCurrentMatches(matches, current_matches):
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
    return current_matches

def buildFinishedMatches(matches):
    finished_matches = {}
    for match in matches:
        match_id = match['id']
        #Add new Matches
        if match['status'] == 'FINISHED':
            oldMatch = Match(match['home_name'],  match['home_id'], match['away_name'], match['score'],  match['time'],  match['location'], match['status'], match['fixture_id']) 
            oldMatch.findCoords()
            finished_matches[match_id] = oldMatch
              
    return finished_matches 

if __name__ == "__main__":
    print(pullSoccerMatches({}))