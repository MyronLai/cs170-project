import annealing, utils
import os, sys, random, math

path = sys.argv[1]
categories = ["small", "medium", "large"]
sample_size = 20
ps_vals = [0, 0.2, 0.4, 0.6, 0.8, 1]
pp_vals = [0, 0.2, 0.4, 0.6, 0.8, 1]
scale_vals = [0.1, 0.01, 0.001, 0.0001, 0.00001]
iters_vals = [1000, 10000, 100000, 1000000]
vals = []
files = os.listdir(path)
for size in categories:
    valid_files = [f"{path}/{file}" for file in files if size in file]
    min_score = math.inf
    min_params = None
    score_vals = []
    for ps in ps_vals:
        for pp in pp_vals:
            for scale in scale_vals:
                for iters in iters_vals:
                    score_tot = 0
                    for i in range(sample_size):
                        chosen = random.choice(valid_files)
                        G = utils.read_input(chosen)
                        print("sampling", chosen)
                        _, score = annealing.anneal(G, iters, ps, pp, scale, print_energy=False)
                        score_tot += score
                    print(f"{size} {ps} {pp} {scale} {iters} {score_tot}")
                    if score_tot < min_score:
                        min_params = (ps, pp, scale, iters)
    print("!!!!!!! MAX OVER {size}: {min_params} --> {min_score}")
