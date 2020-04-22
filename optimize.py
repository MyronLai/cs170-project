#!/usr/bin/python3
import math, heapq
import networkx as nx
import numpy as np
import scipy

# TODO Once best placement found, run better approx algo for MCRT
# TODO Numba

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
