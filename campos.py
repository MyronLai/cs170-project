from heapdict import heapdict
import math

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
                sumWeights += w
    mean = sumWeights/len(edgeSet)
    tempSum = 0
    for u, v, w in edgeSet:
        tempSum += (w - mean)**2
    stdDev = math.sqrt(tempSum/(len(edgeSet) - 1))
    ratio = stdDev / mean
    threshold = 0.4 + 0.005 * (N - 10)
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
    L = heapdict.heapdict()
    L[f] = (0, 0)
    spanned_vertices = 0
    # TODO INIT
    wd = [0] * N
    jsp = [0] * N
    while spanned_vertices < N:
        u, _ = L.popitem()
        for v, weight in graph[u]:
            if colors[v] == -1:
                continue
            wd_t = c4 * weight + c5 * (cf[u] + weight)
            jsp_t = (d[v] + d[u]) + (d[v] + d[u])/(s[v] + s[u])
            if (wd[v], jsp[v]) < (wd_t, jsp_t):
                if colors[v] == 1:
                    wd[v] = wd_t
                    jsp[v] = jsp_t
                    p[v] = u
                    L[v] = (wd[v], jsp[v])
                elif colors[v] == 0:
                    # TODO ??
                    L[v] = (wd[v], jsp[v])
        colors[u] = -1
        spanned_vertices += 1
    return p
