import utils
import annealing
import campos
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

g = utils.read_input("inputs/25.in")
g2 = utils.read_input("inputs/50.in")
g3 = utils.read_input("inputs/100.in")
gsmol = np.ones((5, 5)) - np.eye(5)
gsmol2 = np.ones((10, 10)) - np.eye(10)
gcomp = np.ones((25, 25)) - np.eye(25)
gcomp2 = np.ones((50, 50)) - np.eye(50)
gcomp3 = np.ones((100, 100)) - np.eye(100)

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

def test_output():
    s = annealing.initial_fn(gsmol)
    utils.write_output(gsmol, "/tmp/smol.txt")
    utils.write_output(s, "/tmp/smoltree.txt")

def test_mutate():
    G = gsmol2
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
    print(nx.is_tree(utils.mat_to_nx(s)))
    print(s.shape[0])

    print("Readding")
    state_add = annealing.mutate_fn(state_prune, G, 1, 0)
    plt.figure()
    s = utils.shrink_mat(state_add)
    nx.draw(utils.mat_to_nx(s))
    plt.savefig("/tmp/readded.png")
    print(nx.is_tree(utils.mat_to_nx(s)))
    print(s.shape[0])

    print("Swapping")
    state_swap = annealing.mutate_fn(state_prune, G, 0, 0)
    plt.figure()
    s = utils.shrink_mat(state_swap)
    nx.draw(utils.mat_to_nx(s))
    plt.savefig("/tmp/swapped.png")
    print(nx.is_tree(utils.mat_to_nx(s)))
    print(s.shape[0])

def test_anneal():
    G = g3
    result, score = annealing.anneal(G, 120000, 0.3, 0.5, 0.0004, print_energy=True)
    print(score)
    print("C: ", utils.cost_fn(result))
    nx.draw(utils.mat_to_nx(G))
    plt.savefig("/tmp/g.png")
    plt.figure()
    nx.draw(utils.mat_to_nx(result))
    plt.savefig("/tmp/gres.png")

def test_cost():
    def floyd_warshall_brute_force(weights):
        V = len(weights)
        distance_matrix = weights
        for x in range(V):
            for y in range(V):
                if x != y and distance_matrix[x][y] == 0:
                    distance_matrix[x][y] = 1e99
        for k in range(V):
            next_distance_matrix = [list(row) for row in distance_matrix] # make a copy of distance matrix
            for i in range(V):
                for j in range(V):
                    # Choose if the k vertex can work as a path with shorter distance
                    next_distance_matrix[i][j] = min(distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])
            distance_matrix = next_distance_matrix # update
        return np.sum(distance_matrix)

    G = np.zeros((2, 2))
    print(f"No edges, should be 0: {utils.cost_fn(G)}")

    G[0][1] = 5
    G[1][0] = 5
    print(f"(0)--5--(1), should be 10: {utils.cost_fn(G)}")

    G = np.zeros((5, 5))
    G[0][1] = 3
    G[1][0] = 3
    G[1][2] = 2
    G[2][1] = 2
    G[2][3] = 5
    G[3][2] = 5
    G[2][4] = 4
    G[4][2] = 4
    print(f"5 nodes, 4 edges, should be 120: {utils.cost_fn(G)}")

    for _ in range(10):
        N = np.random.randint(2,50)
        G = np.zeros((N,N))
        for x in range(N):
            for y in range(N):
                G[x][y] = 1 if abs(x-y) == 1 else 0
        print(f"Size {N} line graph, should be {N * (N-1) * (N+1) / 3}: {utils.cost_fn(G)}")
    
    for _ in range(10):
        G = nx.generators.trees.random_tree(np.random.randint(2, 10))
        T = nx.convert_matrix.to_numpy_array(G)
        c = utils.cost_fn(T)
        c2 = floyd_warshall_brute_force(T)
        print(f"Should be {c2}: {c} {c == c2}")
