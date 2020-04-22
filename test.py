import utils
import annealing
import campos
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

g = utils.read_input("inputs/25.in")
g2 = utils.read_input("inputs/50.in")
g3 = utils.read_input("inputs/100.in")
gcomp = np.ones((10, 10))

def test_initial():
    print("Running")
    state = annealing.initial_fn(gcomp)
    print("Done")
    nx.draw(utils.mat_to_nx(state))
    plt.savefig("/tmp/tree.png")
    print(nx.is_tree(utils.mat_to_nx(state)))
    print(np.all(utils.shrink_mat(state) == state))

def test_comp():
    G = np.zeros((6, 6))
    G[0][1] = 1
    G[1][0] = 1
    G[1][2] = 1
    G[2][0] = 1
    G[0][2] = 1
    G[3][4] = 1
    G[4][3] = 1
    print(utils.get_component(G, 1))
    print(utils.get_component(G, 4))
    print(utils.get_component(G, 5))

    nx.draw(utils.mat_to_nx(G))
    plt.savefig("/tmp/g.png")
    plt.figure()
    nx.draw(utils.mat_to_nx(utils.shrink_mat(G)))
    plt.savefig("/tmp/gshrink.png")

def test_mutate():
    G = g
    print("Original")
    state = annealing.initial_fn(G)
    plt.figure()
    nx.draw(utils.mat_to_nx(state))
    plt.savefig("/tmp/original.png")
    print(len(state))

    print("Removing")
    mutate_prune = annealing.make_mutate_fn(1, 1)
    state_prune = mutate_prune(state, G)
    plt.figure()
    nx.draw(utils.mat_to_nx(state_prune))
    plt.savefig("/tmp/pruned.png")
    print(len(state_prune))

    print("Re-adding")
    mutate_add = annealing.make_mutate_fn(1, 0)
    state_add = mutate_add(state_prune, G)
    plt.figure()
    nx.draw(utils.mat_to_nx(state_add))
    plt.savefig("/tmp/readded.png")
    print(len(state_add))

    print("Swapping")
    mutate_swap = annealing.make_mutate_fn(0, 0)
    state_swap = mutate_swap(state_prune, G)
    plt.figure()
    nx.draw(utils.mat_to_nx(state_swap))
    plt.savefig("/tmp/swapped.png")
    print(len(state_swap))

def test_anneal():
    G = g
    result, score = annealing.anneal(G, annealing.initial_fn, annealing.energy_fn, annealing.make_mutate_fn(0.3, 0.5), 120000, 0.0004)
