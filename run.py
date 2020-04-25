import utils
import annealing
import leaderboard
import matplotlib.pyplot as plt
import os, sys
import json
from heapdict import heapdict

def runfile(infile, outfile, score_to_beat = 1e99):
    G = utils.read_input(infile)
    print("Processing", infile)
    result, score = annealing.anneal(G, 120000, 0.2, 0.6, 0.0004, print_energy=False)
    try:
        s = utils.cost_fast(utils.mat_to_nx(utils.shrink_mat(result)))
    except ValueError:
        s = 1e99

    print(f"- {s}")
    if s < score_to_beat:
        utils.write_output(result, G, outfile)
    # assert utils.verify_in_out(G, outfile)
    # TODO REMOVE, Just while fixing bugs
    # os.remove(infile)
    return s


if __name__ == "__main__":
    path = sys.argv[1]
    if not os.path.exists(f"{path}/out"):
        os.mkdir(f"{path}/out")
    print("Running on dir", path)

    top_scores, our_scores, by_input, by_team = leaderboard.parse_leaderboard()    
    try:
        with open(sys.argv[2], "r") as f:
            saved_scores = json.loads(f.read())
        for key in saved_scores:
            if saved_scores[key] < our_scores[key]:
                our_scores[key] = saved_scores[key]
    except IOError:
        for file in os.listdir(path):
            if "." in file and file.split(".")[1] == "in":
                name = file.split('.')[0]
                infile = f"{path}/{file}"
                outfile = f"{path}/out/{name}.out"
                print(f"Running {name}")
                score = runfile(infile, outfile)
                if score < our_scores[name]:
                    print(f"- Improved score from {our_scores[name]} to {score} (-{our_scores[name] - score})")
                    our_scores[name] = score
    
    priorities = heapdict.heapdict({key: (top_scores[key] - our_scores[key]) for key in our_scores})

    print("Running in order of priority")
    try:
        while True:
            name, p = priorities.peekitem()
            to_beat = our_scores[name]
            print(f"Running {name} with priority {p} (our score {to_beat}, top score {top_scores[name]})")
            score = runfile(f"{path}/{name}.in", f"{path}/out/{name}.out", score_to_beat=to_beat)
            if score < to_beat:
                print(f"- Improved score from {to_beat} to {score} (-{to_beat - score})")
                our_scores[name] = score
                priorities[name] = top_scores[name] - score
                with open(sys.argv[2], "w") as f:
                f.write(json.dumps(dict(our_scores)))
            else:
                print(f"- Couldn't improve score (old {to_beat} <= new {score})")
                priorities[name] *= 1.05 if priorities[name] > 0 else 0.95

    except:
        with open(sys.argv[2], "w") as f:
            f.write(json.dumps(dict(our_scores)))
        print(f"Saved scores to {sys.argv[2]}")
