#!/usr/bin/python3
import math, heapq
import networkx as nx
import numpy as np
import scipy

# TODO Once best placement found, run better approx algo for MCRT
# TODO Numba

# http://telecom.inesctec.pt/~rcampos/a-fast-algorithm-for-computing-min-routing-cost-sp.pdf
def campo_mcrt(graph):
    """
    Takes in graph in adjacency list format {u1: [(v1, w1)]}
    Outputs: (cost, edge_list) for MCRT
    """
    # TODO: Possibly speed up with numpy
    N = len(graph)
    d = [0] * N
    s = [0] * N
    m = [0] * N
    sumWeights = 0
    # Make sure only looks at each edge once
    edgeSet = set()
    for u in graph:
        for (v, w) in graph[u]:
            edge = (min(u, v), max(u, v), w)
            if edge not in edgeSet:
                edgeSet.add(edge)
                d[u] += 1
                d[v] += 1
                s[u] += w
                s[v] += w
                m[u] = max(m[u], w)
                m[v] = max(m[v], w)
                sumWeights += weight
    mean = sumWeights/len(edgeSet)
    tempSum = 0
    for u, v, w in edgeSet:
        tempSum += (w - mean)**2
    stdDev = math.sqrt(tempSum/(len(edgeSet) - 1))
    ratio = stdDev / mean
    threshold = 0.4 + 0.005 * (n - 10)
    if ratio < threshold:
        c4 = 1
        c5 = 1
    else:
        c4 = 0.9
        c5 = 0.1

    # WHITE = 1
    # GRAY = 0
    # BLACK = -1
    w = [math.inf] * N
    colors = [1] * N
    sp = [0] * N
    spMax = -math.inf
    f = -1
    for u in graph:
        sp[u] = 0.2*d[u] + 0.6*(d[u]/s[u]) + 0.2/m[u]
        if sp[u] > spMax:
            spMax = sp[u]
            f = v

    cf = [math.inf] * N
    p = [0] * N
    pd = [0] * N
    ps = [0] * N
    w[f] = 0
    cf[f] = 0
    p[f] = f
    pd[f] = 0
    ps[f] = 1
    L = [f]
    spanned_vertices = 0
    while spanned_vertices < N:

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



def cost_fn(nodes):
    return cost(approx_mcrt(nodes))

scipy.optimize.basinhopping(cost_fn, initial_placement, accept_test=check_fn)
