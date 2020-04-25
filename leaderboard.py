import json
import sys

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
    
    our_scores = by_team['jaarn']
    
    return top_scores, our_scores, by_input, by_team

if __name__ == "__main__":
    _, s, _, _ = parse_leaderboard()
    with open(sys.argv[1], "w") as f:
        f.write(json.dumps(s))