import utils
import annealing
import campos
import networkx as nx
import matplotlib.pyplot as plt

g = utils.read_input("inputs/25.in")
g2 = utils.read_input("inputs/50.in")
g3 = utils.read_input("inputs/100.in")

def test_campos():
    t = campos.campo_mcrt(g)
    print(t)
    nx.draw(utils.adj_to_nx(g))
    plt.savefig("/tmp/graph.png", format="PNG")
    plt.figure()
    nx.draw(utils.tree_to_nx(t))
    plt.savefig("/tmp/tree.png", format="PNG")
    print("DRAWN")

def test_initial():
    print("Running")
    state = annealing.initial_fn(g3)
    print("Done")
    nx.draw(utils.adj_to_nx(state))
    plt.savefig("/tmp/tree.png")

def test_comp():
    G = {
        0: [],
        1: [(2, 1), (3, 1)],
        2: [(1, 1)],
        3: [(1, 1)],
        4: [(5, 1)],
        5: [(4, 1)]
    }
    print(annealing.get_component(G, 6, 1))
    print(annealing.get_component(G, 6, 4))

def test_mutate():
    G = g
    print("Original")
    state = annealing.initial_fn(G)
    plt.figure()
    nx.draw(utils.adj_to_nx(state))
    plt.savefig("/tmp/original.png")
    print(len(state))

    print("Removing")
    mutate_prune = annealing.make_mutate_fn(1, 1)
    state_prune = mutate_prune(state, G)
    plt.figure()
    nx.draw(utils.adj_to_nx(state_prune))
    plt.savefig("/tmp/pruned.png")
    print(len(state_prune))

    print("Re-adding")
    mutate_add = annealing.make_mutate_fn(1, 0)
    state_add = mutate_add(state_prune, G)
    plt.figure()
    nx.draw(utils.adj_to_nx(state_add))
    plt.savefig("/tmp/readded.png")
    print(len(state_add))

    print("Swapping")
    mutate_swap = annealing.make_mutate_fn(0, 0)
    state_swap = mutate_swap(state_prune, G)
    plt.figure()
    nx.draw(utils.adj_to_nx(state_swap))
    plt.savefig("/tmp/swapped.png")
    print(len(state_swap))

def test_anneal():
    G = g
    result, score = annealing.anneal(G, annealing.initial_fn, annealing.energy_fn, annealing.make_mutate_fn(0.3, 0.5), 120000, 0.0004)

test_anneal()
