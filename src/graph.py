import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure


MAXVAL = 99999
MINVAL = -99999

def readGraph(filepath):
    with open(filepath, 'r') as f:
        l = [[int(num) for num in line.split(' ')] for line in f]
        return l

def nearestV(dist, spTree, iterations):
    min = MAXVAL+1
    vertex = len(dist)

    for i in range(vertex):
        iterations[0] += 1
        if dist[i] < min and spTree[i] == False:
            min = dist[i]
            min_idx = i
    return min_idx

def dijkstra(graph, src, iterations):


    iterations[0] = 0
    vertex = len(graph)
    path = [[] for _ in range(vertex)]

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
                costStr = [str(j) + "(" + str(dist[j]) + ")"]
                path[j] = [str(src)] + path[i][1:] + costStr
    return dist, path



