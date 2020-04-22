import math
import networkx as nx
import numpy as np

def read_input(file):
    with open(file) as f:
        lines = f.readlines()
    N = int(lines[0])
    g = {}
    for i in range(N):
        g[i] = []
    for line in lines[1:]:
        sp = line.split()
        u, v, w = int(sp[0]), int(sp[1]), int(sp[2])
        g[u].append((v, w))
        g[v].append((u, w))
    return g

def adj_to_nx(g):
    """ Adjacency list to NetworkX """
    G = nx.Graph()
    G.add_nodes_from(g.keys())
    for u in g:
        for v, w in g[u]:
            G.add_edge(u, v, weight=w)
    return G

def tree_to_nx(t):
    """ List of parent pointers to NetworkX  """
    G = nx.Graph()
    G.add_nodes_from(list(range(len(t))))
    for v in t:
        if t[v] != v:
            G.add_edge(v, t[v])
    return G

def create_check_fn(graph):
    def check_fn(nodes):
        tree = [i for i in range(len(nodes)) if nodes[i]]
        touched = set(tree)
        for v in tree:
            s = set([e[0] for e in graph[v]])
            touched.update(s)
        return len(touched) == len(nodes)
    return check_fn

def cost_fn(adj, N):
    # https://www.geeksforgeeks.org/calculate-number-nodes-subtrees-using-dfs/
    # TODO TEST!
    counts = {}
    def count_nodes(s, e):
        counts[s] = 1
        for (u, w) in adj[s]:
            if u == e:
                continue
            count_nodes(u, s)
            counts[s] += counts[u]
    first = next(iter(adj.keys()))
    count_nodes(first, first)
    cost = 0
    for v in adj:
        for u, w in adj[v]:
            min_count = min(counts[v], counts[u])
            cost += 2 * min_count * (N - min_count) * w
    return cost
