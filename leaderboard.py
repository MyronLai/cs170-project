import json
import sys
import math

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
    
    return top_scores, our_scores, calculate_ranks(our_scores, by_input), by_input


def calculate_rank(target_score, inpt, by_input):
    rank = 0
    count = 0
    prev_score = 1e99
    scores = sorted(by_input[inpt].values())
    for score in scores:
        if target_score < score:
            return rank
        count += 1
        if not math.isclose(score, prev_score):
            rank = count
            prev_score = score
        
    return 1 if target_score == 0 else 1e99

def calculate_ranks(our_scores, by_input):
    return {k: calculate_rank(our_scores[k], k, by_input) for k in by_input}


if __name__ == "__main__":
    _, s, _, _ = parse_leaderboard()
    with open(sys.argv[1], "w") as f:
        f.write(json.dumps(s))