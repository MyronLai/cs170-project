import utils
import annealing
import matplotlib.pyplot as plt
import os, sys

path = sys.argv[1]
if not os.path.exists("out"):
    os.mkdir("out")
for file in os.listdir(path):
    if file.split(".")[1] == "in":
        infile = f"{path}/{file}"
        G = utils.read_input(infile)
        print(file, end="")
        result, score = annealing.anneal(G, annealing.initial_fn, annealing.energy_fn, annealing.make_mutate_fn(0.3, 0.5), 120000, 0.0004)
        print(f": {score}")
        outfile = f"{path}/out/{file.split('.')[0]}.out"
        # Remove disconnected nodes because they aren't really part of the state
        shrink_res = utils.shrink_mat(result)
        utils.write_output(shrink_res, outfile)
        # TODO REMOVE, Just while fixing bugs
        os.remove(infile)
