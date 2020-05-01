import math, random
import utils
from numba import njit
from numba.core import types
from numba.typed import Dict
import numpy as np

@njit
def initial_dom_fn(G):
    # Generate "minimum" spanning dominating tree
    state = np.zeros(G.shape)
    min_modified = np.where(G == 0, 1000, G)
    pos = np.argwhere(min_modified == np.min(min_modified))[0]
    u = pos[0]
    v = pos[1]
    # Numba doesn't like random.sample so we use list
    edges = []
    included = set([u, v])
    for neighbor in np.nonzero(G[u])[0]:
        if neighbor != v:
            edges.append((u, neighbor, G[u][neighbor]))
            included.add(neighbor)
    for neighbor in np.nonzero(G[v])[0]:
        if neighbor != u:
            edges.append((v, neighbor, G[v][neighbor]))
            included.add(neighbor)
    marked = np.zeros(G.shape[0])
    marked[u] = 1
    marked[v] = 1
    state[u][v] = G[u][v]
    state[v][u] = G[u][v]
    # Yeah it's slow but it's only run once so it's fine
    # Priority queues are hard
    while len(included) < G.shape[0]:
        curr_min = edges[0]
        w = edges[0][2]
        for e in edges:
            if e[2] < w:
                w = e[2]
                curr_min = e
        u, v, w = curr_min
        edges.remove((u, v, w))
        if not marked[v]:
            marked[v] = True
            state[v][u] = G[u][v]
            state[u][v] = G[u][v]
            for neighbor in np.nonzero(G[v])[0]:
                edges.append((v, neighbor, G[v][neighbor]))
                included.add(neighbor)
    return state

@njit
def initial_span_fn(G):
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

@njit
def initial_fn(G):
    return initial_dom_fn(G)

# Can't be nested because numba
@njit
def mutate_fn(state, G, p_switch, p_prune):
    new_state = np.copy(state)
    # Indicators for nodes which are in state (aka have connections)
    # Should be this: missing = ~G.any(axis=0)
    # But numba doesn't like
    missing = np.zeros(G.shape[0])
    for v in range(G.shape[0]):
        missing[v] = ~np.any(state[v])
    # 1 - because numba doesn't like ~
    present = 1 - missing
    present_vals = np.nonzero(present)[0]
    # Add vertex, remove vertex, or reconfigure edges
    if random.random() < p_switch:
        # Add/Remove vertices
        if random.random() < p_prune:
            # Remove vertex if possible
            k = []
            for v in range(G.shape[0]):
                # Find all leaf state nodes which can be removed
                # TODO WARNING: potentially very slow, n^2? n^3?
                if len(np.nonzero(state[v])[0]) == 1:
                    success = True
                    reached = set()
                    # Make sure all neighbors are reachable from other state nodes
                    for v2 in present_vals:
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
                #print("Checking removal")
                #utils.write_output(new_state, G, "/tmp/res.txt")
                #assert utils.verify_in_out(G, "/tmp/res.txt")
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
                assert False
            else:
                u, v = eligible_edges[np.random.randint(len(eligible_edges))]
                new_state[u][v] = G[u][v]
                new_state[v][u] = G[u][v]
                #print("Checking adding")
                #utils.write_output(new_state, G, "/tmp/res.txt")
                #assert utils.verify_in_out(G, "/tmp/res.txt")
                return new_state
    # Switch only edges around
    # Pick random vertex and disconnect it, reconnecting all components randomly
    v = np.random.choice(present_vals)
    remove_possible_edges = np.nonzero(new_state[v] * present)[0]
    u = remove_possible_edges[np.random.randint(len(remove_possible_edges))]
    # Clears chosen edge on v
    new_state[v][u] = 0
    new_state[u][v] = 0
    comp = utils.get_component(new_state, v)
    complist = list(comp)
    success = False
    while comp:
        chosen = complist[np.random.randint(len(complist))]
        complist.remove(chosen)
        possible_edges = []
        for n2 in np.nonzero(G[chosen])[0]:
            if n2 not in comp and not missing[n2]:
                possible_edges.append(n2)
        if possible_edges:
            chosen_n2 = possible_edges[np.random.randint(len(possible_edges))]
            new_state[chosen][chosen_n2] = G[chosen][chosen_n2]
            new_state[chosen_n2][chosen] = G[chosen][chosen_n2]
            success = True
            break
    if not success:
        print("FAILED TO FIND EDGE! This probably shouldn't happen :(")
    #utils.write_output(new_state, G, "/tmp/res.txt")
    #assert utils.verify_in_out(G, "/tmp/res.txt")
    return new_state

@njit
def check_trivial(G):
    mask = G > 0
    summed = np.sum(mask, axis=0)
    # summed[i] = number of nonzero entries in ith column
    full = (summed >= G.shape[0] - 1)
    # full[i] = ith column is all nonzero (identity connection can be zero)
    val = np.sum(full, axis=0)
    return val > 0

@njit
def anneal(G, iters, p_switch, p_prune, scale, print_energy=False):
    if check_trivial(G):
        return np.zeros(G.shape), 0
    s = initial_fn(G)
    e_init = utils.cost_fn(s)
    e = e_init
    smin, emin = s, e
    # Because some people put empty graphs to start with smh
    if e == 0:
        return smin, emin
    for k in range(iters):
        temp = (k + 1) / iters
        s_new = mutate_fn(s, G, p_switch, p_prune)
        e_new = utils.cost_fn(s_new)
        # Normalize with e_init because different graphs have different weights
        if e_new < e or random.random() < math.exp(-(e_new - e)*temp*scale/e_init):
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
