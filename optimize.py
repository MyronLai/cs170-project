#!/usr/bin/python3
import math, heapq
import networkx as nx
import numpy as np
from scipy import optimize
import scipy

# TODO Once best placement found, run better approx algo for MCRT
# TODO Numba

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
    G.add_nodes_from(list(range(len(g))))
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

def genetic_mcrt(graph):
    pass

def create_check_fn(graph):
    def check_fn(nodes):
        tree = [i for i in range(len(nodes)) if nodes[i]]
        touched = set(tree)
        for v in tree:
            s = set([e[0] for e in graph[v]])
            touched.update(s)
        return len(touched) == len(nodes)
    return check_fn


def cost_fn(adj):
    counts = [0] * len(edges)

    # https://www.geeksforgeeks.org/calculate-number-nodes-subtrees-using-dfs/
    def count_nodes(s, e):
        counts[s] = 1
        for (u, w) in adj[s]:
            if u == e:
                continue

            count_nodes(u, s)
            counts[s] += counts[u]
    
    count_nodes(0, 0)

    # I think this is right but my brain just broke and it might not be idk
    # Mostly not sure about the weights[i] part
    cost = 0
    for i in range(len(edges)):
        cost += 2 * counts[i] * (len(edges) - counts[i]) * weights[i]

    return cost
    


scipy.optimize.basinhopping(cost_fn, initial_placement, accept_test=check_fn)
