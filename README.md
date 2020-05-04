# CS 170 Project <!-- omit in toc -->

**Table of Contents**
- [Algorithm Description](#algorithm-description)
- [Dependencies](#dependencies)
- [Run Instructions](#run-instructions)
  - [Running All Inputs](#running-all-inputs)
  - [Running Based on Rank Priority](#running-based-on-rank-priority)

## Algorithm Description

We used simulated annealing in order to produce outputs. For each input, we generate a random initialization state, which is a valid output for the provided graph. We then randomly mutate the state, which chooses to either add/remove vertices from the state (while still keeping it a valid output) or swap edges on a vertex. New states are “accepted” if their cost is lower or with a random probability decreasing with higher cost. In this way, the cost is allowed to jump around to potentially higher states in order to escape local minima. After a certain number of iterations, the algorithm outputs the lowest-cost state found. This seemed like a reasonable approach because it tries to strike a balance between “exploitation” and “exploration”: the algorithm seeks to find the global minimum cost by preferring lower-cost states but also having some chance of accepting a higher-cost state (allowing the algorithm to “restart” a bit an becoming less likely to get stuck in a ditch).

## Dependencies

The following python packages are required to run this program. All can be obtained from PyPi through `pip`:

- `networkx`
- `numba` (to improve speed)
- `numpy`
- `matplotlib`
- `heapdict` (python has no built-in priority queue)

## Run Instructions

After installing all dependencies, create a directory containing all of the inputs (we'll refer to this directory as `inputs`)

Once you have the inputs set up, there are two options for running the program:

### Running All Inputs

To generate an output for each input, run the following command:

`python3 run.py <inputs directory> <path to output scores.json>`

Example: `python3 run.py inputs scores.json`

This will run through each input, generating an output file corresponding to each input in `inputs/out/input-name.out` (for example the input `inputs/small-100.in` would generate the output `inputs/out/small-100.out`)

The program will also output a `scores.json` file, which is a dictionary of input name to score

After running through each input once, the program will terminate

### Running Based on Rank Priority

Optionally, instead of running through all possible inputs, the program can run inputs in an order based on our team's current rank on the leaderboard. This causes it to run inputs we are bad at more often, hopefully generating an improvement. This requires a little bit of setup.

First, generate a `scores.json` file in one of two ways:

1. Run all inputs as described [above](#running-all-inputs)
2. Run `python3 leaderboard.py scores.json` (this will generate a `scores.json` based on our scores on the saved version of the leaderboard)
   
Once the `scores.json` file has been generated, run the following:

`python3 run.py <input directory> <path to scores.json>`

Example: `python3 run.py inputs scores.json`

This will run the inputs based on rank, with worse ranks having a higher priority. The program will never terminate on its own, however you can stop it at any time using `Ctrl+C` and it will save its progress.