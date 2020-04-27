import json
import sys

OUR_TEAM_NAME = 'jaarn'

def parse_leaderboard():
    with open("leaderboard.json", "r") as l:
        j = json.loads(l.read())

    by_team = {}
    by_input = {}
    top_scores = {}

    data = j['d']['b']['d']
    
    for key in data:
        team = data[key]["leaderboard_name"]
        inpt = data[key]["input"]
        score = float(data[key]["score"])
        if team not in by_team:
            by_team[team] = {}
        if inpt not in by_input:
            by_input[inpt] = {}
        if inpt not in top_scores:
            top_scores[inpt] = 1e99
        by_team[team][inpt] = score
        by_input[inpt][team] = score
        top_scores[inpt] = min(top_scores[inpt], score)
    
    our_scores = by_team[OUR_TEAM_NAME]
    
    return top_scores, our_scores, calculate_ranks(by_input), by_input


def calculate_rank(inpt, by_input):
    rank = 0
    count = 0
    prev_score = 1e99
    teams = sorted(by_input[inpt].items(), key=lambda kvp: kvp[1])
    for team, score in teams:
        count += 1
        if score != prev_score:
            rank = count
            prev_score = score
        if team == OUR_TEAM_NAME:
            return rank
        
    return 1e99

def calculate_ranks(by_input):
    return {k: calculate_rank(k, by_input) for k in by_input}


if __name__ == "__main__":
    _, s, _, _ = parse_leaderboard()
    with open(sys.argv[1], "w") as f:
        f.write(json.dumps(s))