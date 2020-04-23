import utils
import annealing
import matplotlib.pyplot as plt
import os, sys

path = sys.argv[1]
if not os.path.exists(f"{path}/out"):
    os.mkdir(f"{path}/out")
print("Running on dir", path)
for file in os.listdir(path):
    if file.split(".")[1] == "in":
        infile = f"{path}/{file}"
        G = utils.read_input(infile)
        print("Processing", file)
        result, score = annealing.anneal(G, 120000, 0.2, 0.6, 0.0004, print_energy=False)
        print(f"- {score}")
        outfile = f"{path}/out/{file.split('.')[0]}.out"
        utils.write_output(result, G, outfile)
        # TODO REMOVE, Just while fixing bugs
        os.remove(infile)
