import math
import networkx as nx
import numpy as np
from numba import njit

# numba does not like this for some reason
def read_input(file):
    """ Read adjacency matrix from input
        N
        U1 V2 W1
        U2 V2 W2
        ...
    """
    with open(file) as f:
        lines = f.readlines()
    N = int(lines[0])
    g = np.zeros((N, N))
    for line in lines[1:]:
        sp = line.split()
        u, v, w = int(sp[0]), int(sp[1]), float(sp[2])
        g[u][v] = w
        g[v][u] = w
    return g

def write_output(G, file):
    """ Write adjacency matrix to input
        V1 V2 V3 ...
        U1 V1
        U2 V2
        ...
    """
    lines = []
    lines.append("")
    present = set()
    s = set()
    for u in range(G.shape[0]):
        for v in np.nonzero(G[u])[0]:
            present.add(u)
            present.add(v)
            minu, minv = min(u, v), max(u, v)
            if (minu, minv) not in s:
                v = str(minu) + " " + str(minv) + "\n"
                lines.append(v)
                s.add((minu, minv))
    lines[0] = " ".join([str(v) for v in present]) + "\n"
    with open(file, "w") as f:
        f.writelines(lines)

# numba does not like this for some reason
def shrink_mat(G):
    """ Returns a new adjacency matrix with all the zero rows/columns (disconnected nodes) removed """
    Grem = G[~np.all(G == 0, axis=0)]
    Grem = Grem[~np.all(Grem == 0, axis=1)]
    return Grem

def mat_to_nx(G):
    """ Adjacency matrix to NetworkX """
    g = nx.Graph()
    g.add_nodes_from(list(range(G.shape[0])))
    s = set()
    for u in range(G.shape[0]):
        for v in np.nonzero(G[u])[0]:
            minu, minv = min(u, v), max(u, v)
            if (minu, minv) not in s:
                g.add_edge(minu, minv, weight=G[minu][minv])
                s.add((minu, minv))
    return g

@njit
def get_component(G, start):
    """ Get all nodes in the connected component around start """
    visited = np.zeros(G.shape[0])
    stack = [start]
    nodes = set()
    while stack:
        curr = stack.pop()
        visited[curr] = True
        nodes.add(curr)
        for v in np.nonzero(G[curr])[0]:
            if not visited[v]:
                stack.append(v)
    return nodes

@njit
def count_nodes(G, s, e, counts):
    counts[s] = 1
    for u in np.nonzero(G[s])[0]:
        if u == e:
            continue
        count_nodes(G, u, s, counts)
        counts[s] += counts[u]

@njit
def cost_fn(G):
    # https://www.geeksforgeeks.org/calculate-number-nodes-subtrees-using-dfs/
    # TODO TEST!
    # Return 0 for empty graph
    if not np.any(G):
        return 0
    counts = np.zeros(G.shape[0])
    first = np.nonzero(G)[0][0]
    count_nodes(G, first, first, counts)
    cost = 0
    for u in range(G.shape[0]):
        for v in np.nonzero(G[u])[0]:
            min_count = min(counts[v], counts[u])
            # Don't multiply by 2 since each edge is counted twice anyways
            cost += min_count * (G.shape[0] - min_count) * G[u][v]
    return cost
