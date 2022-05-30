from dis import dis
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure


MAXVAL = 9999
MINVAL = -9999

file = open('g2.txt', 'r')

def readGraph(filepath):
    with open(filepath, 'r') as f:
        l = [[int(num) for num in line.split(' ')] for line in f]
        return l

def drawGraph(graph):
    # fig = Figure()
    G = nx.DiGraph()
    length = len(graph)
    for i in range(length):
        for j in range(length):
            if graph[i][j] != 0:
               G.add_edge(str(i), str(j), weight=graph[i][j])
    
    e = [(u, v) for (u, v, d) in G.edges(data=True)]

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(
        G, pos, edgelist=e, width=6, edge_color="g", arrowstyle="->", arrowsize=20,
    )

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    # ax = plt.gca()
    # ax.margins(0.08)
    # plt.axis("off")
    # plt.tight_layout()
    plt.show()

def nearestV(dist, spTree, iterations):
    min = MAXVAL
    vertex = len(dist)

    for i in range(vertex):
        iterations[0] += 1
        if dist[i] < min and spTree[i] == False:
            min = dist[i]
            min_idx = i
    return min_idx

def printSolution(dist):
    vertex = len(dist)
    print("Vertex \tDistance from Source")
    for node in range(vertex):
        print(node, "\t", dist[node])

def dijkstra(graph, src, iterations):
    iterations[0] = 0
    vertex = len(graph)

    dist = [MAXVAL] * vertex
    dist[src] = 0
    spTree = [False] * vertex

    for a in range(vertex):
        i = nearestV(dist, spTree, iterations)

        spTree[i] = True

        for j in range(vertex):
            iterations[0] += 1
            if graph[i][j] > 0 and spTree[j] == False and dist[j] > dist[i] + graph[i][j]:
                dist[j] = dist[i] + graph[i][j]
    print(dist)
    return dist

        




# graph = readGraph("g3.txt")

# print(graph)

# drawGraph(graph)
# dijkstra(graph, 0)




