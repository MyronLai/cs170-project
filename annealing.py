import math, random
import optimize

def initial_fn(G):
    # Generate random spanning tree
    # Choose random root node, expand tree out randomly
    # TODO This can be slow
    state = {}
    for v in G:
        state[v] = []
    marked = [False] * len(G)
    visited = 1
    curr = random.randrange(len(G))
    marked[curr] = True
    edges = [(curr, x[0], x[1]) for x in G[curr]]
    while visited < len(G):
        u, v, w = random.choice(list(edges))
        edges.remove((u, v, w))
        if not marked[v]:
            marked[v] = True
            state[v].append((u, w))
            state[u].append((v, w))
            edges.extend([(v, x[0], x[1]) for x in G[v]])
            visited += 1
    return state

def energy_fn(state, G):
    # Minimize energy = maximize cost
    return -optimize.cost_fn(state, len(G))

def get_component(G, N, start):
    visited = [False] * N
    stack = [start]
    nodes = set()
    while stack:
        curr = stack.pop()
        visited[curr] = True
        nodes.add(curr)
        for v, _ in G[curr]:
            if not visited[v]:
                stack.append(v)
    return nodes

# TODO: Consider optimizing with sets instead of adj. list
# Don't store weight in graph directly, have separate list?
# WARNING: Don't use len(state) as range usually, things aren't guaranteed to be consecutive
# WARNING: CAN ONLY USE len(G) as range IF IT'S NOT A STATE (see above fn, needs extra N)
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
                        reached = set()
                        # Make sure all neighbors are reachable from other state nodes
                        for v2 in state:
                            if v2 != v:
                                for neighbor, _ in G[v2]:
                                    if neighbor not in reached:
                                        reached.add(neighbor)
                        for neighbor, _ in G[v]:
                            if neighbor not in reached:
                                success = False
                                break
                        if success:
                            k.append(v)
                # Pick one
                # If none possible, bail out to next case
                if k:
                    # Remove v from new state with no repercussions
                    v = random.choice(k)
                    del new_state[v]
                    for vert, w in state[v]:
                        new_state[vert].remove((v, w))
                        # Removes other vertex too if it's not necessary
                        if len(new_state[vert]) == 0:
                            del new_state[vert]
                    return new_state
            # Add vertex if possible
            # If none possible, bail out to next case
            if len(state.keys()) < len(G):
                missing = set(G.keys()) - set(state.keys())
                eligible_edges = []
                # Pick an EDGE from the ones connecting any missing node to state nodes
                for m in missing:
                    for neighbor, w in G[m]:
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
        v = random.choice(list(state.keys()))
        # Clears all edges on v
        new_state[v] = []
        for vert, w in state[v]:
            new_state[vert].remove((v, w))
        # Adds edges between all connected components
        incorporated = set([v])
        # Possible edges to other components
        curr_edges = [(v, x[0], x[1]) for x in G[v] if x[0] in state.keys()]
        add_edges = []
        while len(incorporated) < len(state):
            # Pick an edge randomly
            u, v, w = random.choice(curr_edges)
            curr_edges.remove((u, v, w))
            # If the connected component isn't absorbed, use it
            if v not in incorporated:
                add_edges.append((u, v, w))
                # Add all the elements in the component to the visited set
                comp = get_component(new_state, len(G), v)
                incorporated = incorporated.union(comp)
                # Add all the edges coming off the component into a non-visited set
                for neighbor in comp:
                    for n2, w in G[neighbor]:
                        if n2 not in incorporated and n2 in state.keys():
                            curr_edges.append((neighbor, n2, w))
        for u, v, w in add_edges:
            new_state[u].append((v, w))
            new_state[v].append((u, w))
        return new_state
    return mutate_fn

def anneal(G, initial_fn, energy_fn, mutate_fn, iters):
    s = initial_fn(G)
    e = energy_fn(s, G)
    min_s, e_min = s, e
    for k in range(iters):
        temp = (k + 1) / iters
        s_new = mutate_fn(s, G)
        e_new = energy_fn(s_new, G)
        if e_new < e or math.exp(-(e_new - e)*temp) < random.random():
            s = s_new
            e = e_new
            print(e)
            if e < e_min:
                mins = s
                e_min = e
    return min_s, e_min
