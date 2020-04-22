import math, random
import utils
from numba import njit
from numba.core import types
from numba.typed import Dict
import numpy as np

@njit
def initial_fn(G):
    # Generate random spanning tree
    # Choose random root node, expand tree out randomly
    state = np.zeros(G.shape)
    marked = np.zeros(G.shape[0])
    visited = 1
    curr = np.random.randint(G.shape[0])
    marked[curr] = 1
    # Numba doesn't like random.sample so we use list
    edges = []
    for neighbor in np.nonzero(G[curr])[0]:
        edges.append((curr, neighbor))
    while visited < G.shape[0]:
        u, v = edges[np.random.randint(len(edges))]
        edges.remove((u, v))
        if not marked[v]:
            marked[v] = True
            state[v][u] = G[u][v]
            state[u][v] = G[u][v]
            for neighbor in np.nonzero(G[v])[0]:
                edges.append((v, neighbor))
            visited += 1
    return state

# Can't be nested because numba
@njit
def mutate_fn(state, G, p_switch, p_prune):
    new_state = np.copy(state)
    # Indicators for nodes which are in state (aka have connections)
    # Should be this: missing = ~G.any(axis=0)
    # But numba doesn't like
    missing = np.zeros(G.shape[0])
    for v in range(G.shape[0]):
        missing[v] = ~np.any(G[v])
    # Add vertex, remove vertex, or reconfigure edges
    if random.random() < p_switch:
        # Add/Remove vertices
        if random.random() < p_prune:
            # Remove vertex if possible
            k = []
            for v in range(G.shape[0]):
                # Find all leaf state nodes which can be removed
                # TODO WARNING: potentially very slow, n^2? n^3?
                if len(np.nonzero(G[v])) == 1:
                    success = True
                    reached = set()
                    # Make sure all neighbors are reachable from other state nodes
                    for v2 in range(G.shape[0]):
                        if v2 != v:
                            for neighbor in np.nonzero(G[v2])[0]:
                                if neighbor not in reached:
                                    reached.add(neighbor)
                    for neighbor in np.nonzero(G[v])[0]:
                        if neighbor not in reached:
                            success = False
                            break
                    if success:
                        k.append(v)
            # Pick one
            # If none possible, bail out to next case
            if k:
                # Remove v from new state with no repercussions
                v = k[np.random.randint(len(k))]
                new_state[v] = np.zeros(G.shape[0])
                new_state[:, v] = np.zeros(G.shape[0])
                return new_state
        # Check if all vertices are in state
        # Add vertex if possible
        # If none possible, bail out to next case
        if np.any(missing):
            eligible_edges = []
            # Pick an EDGE from the ones connecting any missing node to state nodes
            for m in np.nonzero(missing)[0]:
                for neighbor in np.nonzero(G[m])[0]:
                    if not missing[neighbor]:
                        eligible_edges.append((m, neighbor))
            if not eligible_edges:
                # Shouldn't happen I think
                print("================================")
                print("This is probably bad, the graph should be connected")
                print(state)
                print(G)
                print("================================")
                return new_state
            else:
                u, v = eligible_edges[np.random.randint(len(eligible_edges))]
                new_state[u][v] = G[u][v]
                new_state[v][u] = G[u][v]
                return new_state
    # Switch only edges around
    # Pick random vertex and disconnect it, reconnecting all components randomly
    # 1 - because numba doesn't like ~
    present = 1 - missing
    present_vals = np.nonzero(present)[0]
    v = np.random.choice(present_vals)
    # Clears all edges on v
    new_state[v] = np.zeros(G.shape[0])
    new_state[:, v] = np.zeros(G.shape[0])
    # Adds edges between all connected components
    incorporated = set([v])
    # Possible edges to other components
    curr_edges = []
    for neighbor in np.nonzero(G[v])[0]:
        curr_edges.append((v, neighbor))
    while len(incorporated) < len(state):
        # Pick an edge randomly
        if not curr_edges:
            print("RAN OUT OF EDGES!! Probably shouldn't happen :/")
        u, v = curr_edges[np.random.randint(len(curr_edges))]
        curr_edges.remove((u, v))
        # If the connected component isn't absorbed, use it
        if v not in incorporated:
            # Add the edge to the state
            new_state[u][v] = G[u][v]
            new_state[v][u] = G[u][v]
            # Add all the elements in the component to the visited set
            comp = utils.get_component(new_state, v)
            incorporated = incorporated.union(comp)
            # Add all the edges coming off the component into a non-visited set
            for neighbor in comp:
                for n2 in np.nonzero(G[neighbor])[0]:
                    if n2 not in incorporated and not missing[n2]:
                        curr_edges.append((neighbor, n2))
    return new_state

@njit
def anneal(G, iters, p_switch, p_prune, scale, print_energy=False):
    s = initial_fn(G)
    e = utils.cost_fn(s)
    smin, emin = s, e
    for k in range(iters):
        temp = (k + 1) / iters
        s_new = mutate_fn(s, G, p_switch, p_prune)
        e_new = utils.cost_fn(s_new)
        if e_new < e or random.random() < math.exp(-(e_new - e)*temp*scale):
            s = s_new
            e = e_new
            if print_energy:
                print(e)
            if e < emin:
                smin = s
                emin = e
                # No state nodes messes up the function, can't get better than 0 anyways
                if e == 0:
                    break
    return smin, emin
