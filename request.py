import requests
import json

def pullFinishedSoccerMatches(current_matches, date):
    key = 'dovU4iInbWpHnIHs'
    secret = '0kKYErWnwnA61f1eDw9IOR50OvHbdpEd'
    url = f"http://livescore-api.com/api-client/scores/history.json?from={date}&to={date}&key={key}&secret={secret}"
    matches = []
    page = 1
    while True:
        response = requests.get(url + f'&page={page}')
        print(response)
        data = response.json()
        if data:
            matches.extend(data['data']['match'])
            if data['data']['next_page']:
                page += 1
            else:
                break  
    return matches
    # for match in matches:
    #     match_id = match['id']
    #     #Add new Matches
    #     if match_id not in current_matches and match['status'] == 'FINISHED':
    #         curMatch = Match(match['home_name'],  match['home_id'], match['away_name'], match['score'],  match['time'],  match['location'], match['status'], match['fixture_id']) 
    #         curMatch.findCoords()
    #         current_matches[match_id] = curMatch   
    
    # return current_matches              

if __name__ == "__main__":
    print(pullFinishedSoccerMatches({}, '2020-03-04'))