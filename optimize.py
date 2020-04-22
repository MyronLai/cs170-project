#!/usr/bin/python3
import networkx as nx
import numpy as np
import scipy


def campo_mcrt(graph):
    N = sizeof(graph)
    d = [0] * N
    s = [0] * N
    m = [0] * N
    sumWeights = 0
    # TODO Make sure only looks at each edge once
    for (i, j, weight) in edges:
        d[i] += 1
        d[j] += 1
        s[i] += weight
        s[j] += weight
        m[i] = max(m[i], weight)
        m[j] = max(m[j], weight)
        sumWeights += weight
    mean = sumWeights / len(edges)


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
