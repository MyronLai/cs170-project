import matplotlib.pyplot as plt
import networkx as nx
import math
import random

NP = [(100, 0.6, 0.1), (25, 0.9, 0.15), (50, 0.8, 0.105)]

def print_graph(G):
    zop = []
    NS = str(G.number_of_nodes())
    zop.append(NS + "\n")
    conn = nx.to_edgelist(G)
    for (u, v, _) in conn:
        zop.append(f"{u} {v} {random.randint(1, 99)}\n")
    with open(NS + ".in", "w") as f:
        f.writelines(zop)

for (N, b, a) in NP:
    while True:
        G = nx.waxman_graph(2)
        while not nx.is_connected(G):
            G = nx.waxman_graph(N, b, a)
        nx.draw(G)
        plt.show()
        if input() == "yes":
            print_graph(G)
            break
