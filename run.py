import utils
import annealing
import matplotlib.pyplot as plt
import os, sys


def runfile(infile, outfile):
    G = utils.read_input(infile)
    print("Processing", infile)
    result, score = annealing.anneal(G, 120000, 0.2, 0.6, 0.0004, print_energy=False)
    print(f"- {score}")
    utils.write_output(result, G, outfile)
    assert utils.verify_in_out(G, outfile)
    # TODO REMOVE, Just while fixing bugs
    #os.remove(infile)

if __name__ == "__main__":
    path = sys.argv[1]
    if not os.path.exists(f"{path}/out"):
        os.mkdir(f"{path}/out")
    print("Running on dir", path)
    for file in os.listdir(path):
        if file.split(".")[1] == "in":
            infile = f"{path}/{file}"
            outfile = f"{path}/out/{file.split('.')[0]}.out"
            runfile(infile, outfile)
