import utils
import annealing
import campos
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

g = utils.read_input("inputs/25.in")
g2 = utils.read_input("inputs/50.in")
g3 = utils.read_input("inputs/100.in")
gsmol = np.ones((5, 5))
gcomp = np.ones((25, 25))
gcomp2 = np.ones((50, 50))
gcomp3 = np.ones((100, 100))

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
    G = gcomp
    print("Original")
    state = annealing.initial_fn(G)
    plt.figure()
    s = utils.shrink_mat(state)
    nx.draw(utils.mat_to_nx(s))
    plt.savefig("/tmp/original.png")
    print(s.shape[0])

    print("Removing")
    state_prune = annealing.mutate_fn(state, G, 1, 1)
    plt.figure()
    s = utils.shrink_mat(state_prune)
    nx.draw(utils.mat_to_nx(s))
    plt.savefig("/tmp/pruned.png")
    print(s.shape[0])

    print("Readding")
    state_add = annealing.mutate_fn(state_prune, G, 1, 0)
    plt.figure()
    s = utils.shrink_mat(state_add)
    nx.draw(utils.mat_to_nx(s))
    plt.savefig("/tmp/readded.png")
    print(s.shape[0])

    print("Swapping")
    state_swap = annealing.mutate_fn(state_prune, G, 0, 0)
    plt.figure()
    s = utils.shrink_mat(state_swap)
    nx.draw(utils.mat_to_nx(s))
    plt.savefig("/tmp/swapped.png")
    print(s.shape[0])

def test_anneal():
    G = g
    result, score = annealing.anneal(G, 120000, 0.3, 0.5, 0.0004, print_energy=True)
