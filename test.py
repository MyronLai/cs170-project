import optimize
import campos
import networkx as nx
import matplotlib.pyplot as plt

g = optimize.read_input("inputs/25.in")
t = campos.campo_mcrt(g)
print(t)
nx.draw(optimize.adj_to_nx(g))
plt.savefig("/tmp/Graph.png", format="PNG")
plt.figure()
nx.draw(optimize.tree_to_nx(t))
plt.savefig("/tmp/Tree.png", format="PNG")
print("DRAWN")
