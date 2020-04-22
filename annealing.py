import math, random
import disjoint_set

def initial_fn(G):
    # Random walk to generate random spanning tree
    # TODO This can be slow
    state = {}
    for v in G:
        state[v] = []
    marked = [False] * len(G)
    visited = 1
    curr = random.randrange(len(G))
    marked[curr] = True
    while visited < len(G):
        next_val, w = random.choice(G[curr])
        if not marked[next_val]:
            marked[next_val] = True
            state[next_val].append((curr, w))
            state[curr].append((next_val, w))
            curr = next_val
            visited += 1
    return state

def energy_fn(state):
    # Minimize energy = maximize cost
    return -optimize.cost_fn(state)

def get_component(G, n):
    visited = [False] * len(G)
    stack = [n]
    nodes = set()
    while stack:
        curr = stack.pop()
        visited[curr] = True
        nodes.add(curr)
        for v, _ in G[curr]:
            if not visited[v]:
                visited.append(v)
    return nodes

# TODO: Consider optimizing with sets instead of adj. list
# Don't store weight in graph directly, have separate list?
def make_mutate_fn(p_switch, p_prune):
    def mutate_fn(state, G):
        new_state = {}
        for v in state:
            new_state[v] = state[v].copy()
        # Add vertex, remove vertex, or reconfigure edges
        if random.random() < p_switch:
            # Add/Remove vertices
            if random.random() < p_prune:
                # Remove vertex if possible
                # Find all leaf state nodes which can be removed
                # TODO WARNING: potentially very slow, n^2? n^3?
                k = []
                for v in state:
                    if len(state[v]) == 1:
                        success = True
                        for neighbor, _ in G[v]:
                            # Make sure all neighbors are reachable from other state nodes
                            for v2 in state:
                                if v2 != v:
                                    # TODO
                # Pick one
                # If none possible, bail out to next case
                if k:
                    # Remove v from new state with no repercussions
                    v = random.choice(k)
                    new_state[v] = []
                    for vert, w in state[v]:
                        new_state[vert].remove((v, w))
                    return new_state
            # Add vertex if possible
            # If none possible, bail out to next case
            if len(state) < len(G):
                missing = set(G.keys()) - set(state.keys())
                eligible_edges = []
                # Pick an EDGE from the ones connecting any missing node to state nodes
                for m in missing:
                    for neighbor, w in G[missing]:
                        if neighbor in state:
                            eligible_edges.append((m, neighbor, w))
                u, v, w = random.choice(eligible_edges)
                if not eligible_edges:
                    # Shouldn't happen I think
                    print("================================")
                    print("This is probably bad, the graph should be connected")
                    print(state)
                    print(G)
                    print("================================")
                    return new_state
                else:
                    new_state[u] = [(v, w)]
                    new_state[v].append((u, w))
                    return new_state
        # Switch only edges around
        # Pick random vertex and disconnect it, reconnecting all components randomly
        # TODO Kinda slow?
        v = random.choice(len(state)) # Must be state because it might not include all
        # Clears all edges on v
        new_state[v] = []
        for vert, w in state[v]:
            new_state[vert].remove((v, w))
        # Adds edges between all connected components
        add_edges = []
        considered = set()
        TODO DOES NOT WORK
        #for vert, w in state[v]:
        #    comp = get_component(new_state, vert)
        #    considered = considered.union(comp)
        return new_state
    return mutate_fn

def anneal(G, initial_fn, energy_fn, mutate_fn, iters):
    s = initial_fn(G)
    e = energy_fn(s)
    min_s, e_min = s, e
    for k in range(iters):
        temp = (k + 1) / iters
        s_new = mutate_fn(G, s)
        e_new = energy_fn(s_new)
        if e_new < e or math.exp(-(e_new - e)*temp) < random.random():
            s = s_new
            e = e_new
            print(e)
            if e < e_min:
                mins = s
                e_min = e
    return min_s, e_min
