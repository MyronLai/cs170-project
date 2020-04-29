import sys
import os
import json
import numpy as np

if __name__ == "__main__":
    paths = sys.argv[1:]

    inputs = {}
    output = [(0,",".join(["Input"] + [str(i) for i in range(1, 1 + len(paths))]))]

    for path in paths:
        with open(path, "r") as f:
            j = json.loads(f.read())
        for key in j:
            if key not in inputs:
                inputs[key] = []
            inputs[key].append(j[key])

    for inpt, scores in inputs.items():
        s = int(inpt.split('-')[1])
        if "large" in inpt:
            s += 1000
        elif "medium" in inpt:
            s += 500
        l = [str(x) for x in list(np.sort(scores)[::-1].round(decimals=5))]
        output.append((s, ",".join([inpt] + l)))

    for line in sorted(output, key=lambda t: t[0]):
        print(line[1])