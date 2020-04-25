import math
import networkx as nx
import numpy as np
from numba import njit
from collections import defaultdict
import sys

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

# numba does not like
def write_output(G, G_orig, file):
    """ Write adjacency matrix to output
        If matrix is empty, find single vertex which is connected to others
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
    if len(present) == 0:
        success = False
        for v in range(G.shape[0]):
            # If connected to everything (or all but itself technically)
            if np.sum(G_orig[v] == 0) <= 1:
                lines[0] = str(v) + "\n"
                success = True
                break
        if not success:
            print("FAILED TO FIND VALID VERTEX!!!")
            sys.exit(1)
    else:
        lines[0] = " ".join([str(v) for v in present]) + "\n"
    with open(file, "w") as f:
        f.writelines(lines)

def verify_in_out(G, outfile):
    with open(outfile) as f:
        lines = f.readlines()
    verts = [int(x) for x in lines[0].split(" ")]
    g = nx.Graph()
    g.add_nodes_from(verts)
    for line in lines[1:]:
        sp = line.split(" ")
        v1, v2 = int(sp[0]), int(sp[1])
        g.add_edge(v1, v2)
    if not nx.is_tree(g):
        print("Not tree!")
        return False
    for v in range(G.shape[0]):
        if v not in verts:
            success = False
            for v2 in verts:
                if G[v][v2]:
                    success = True
                    break
            if not success:
                print("Not everything is connected!", v)
                return False
    print("Successfully verified!")
    return True

# numba does not like
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
# https://www.geeksforgeeks.org/calculate-number-nodes-subtrees-using-dfs/
def count_nodes(G, s, e, counts):
    counts[s] = 1
    for u in np.nonzero(G[s])[0]:
        if u == e:
            continue
        count_nodes(G, u, s, counts)
        counts[s] += counts[u]

@njit
def cost_fn(G):
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
            cost += min_count * (np.count_nonzero(np.sum(G, axis=0)) - min_count) * G[u][v]
    return cost

def cost_fast(T):
    """Calculates the average pairwise distance for a tree in linear time.
    Since there is always unique path between nodes in a tree, each edge in the
    tree is used in all of the paths from the connected component on one side
    of the tree to the other. So each edge contributes to the total pairwise cost
    in the following way: if the size of the connected components that are
    created from removing an edge e are A and B, then the total pairwise distance
    cost for an edge is 2 * A * B * w(e) = (# of paths that use that edge) * w(e).
    We multiply by two to consider both directions that paths can take on an
    undirected edge.
    Since each edge connects a subtree to the rest of a tree, we can run DFS
    to compute the sizes of all of the subtrees, and iterate through all the edges
    and sum the pairwise distance costs for each edge and divide by the total
    number of pairs.
    This is very similar to Q7 on MT1.
    h/t to Noah Kingdon for the algorithm.
    """
    if len(T) <= 1: return 0

    if not nx.is_connected(T):
        raise ValueError("Tree must be connected")

    subtree_sizes = {}
    marked = defaultdict(bool)
    # store child parent relationships for each edge, because the components
    # created when removing an edge are the child subtree and the rest of the vertices
    root = list(T.nodes)[0];
    
    child_parent_pairs = [(root, root)]

    def calculate_subtree_sizes(u):
        """Iterates through the tree to compute all subtree sizes in linear time
        Args:
            u: the root of the subtree to start the DFS
        """
        unmarked_neighbors = filter(lambda v: not marked[v], T.neighbors(u))
        marked[u] = True
        size = 0
        for v in unmarked_neighbors:
            child_parent_pairs.append((v, u))
            calculate_subtree_sizes(v)
            size += subtree_sizes[v]
        subtree_sizes[u] = size + 1
        return subtree_sizes[u]

    calculate_subtree_sizes(root)  # any vertex can be the root of a tree

    cost = 0
    for c, p in child_parent_pairs:
        if c != p:
            a, b = subtree_sizes[c], len(T.nodes) - subtree_sizes[c]
            w = T[c][p]["weight"]
            cost += 2 * a * b * w
    return cost / (len(T) * (len(T) - 1))