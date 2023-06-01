# Classe representando um grafo por matriz de adjacencia, e métodos para o algoritmo de Kruskal
class Graph:
    INF = float("inf")

    def __init__(self, G=None, vertex=0):
        # Grafo reperesentado por matriz de adjacência
        self.graph = []
        self.parent = []

        if G:
            self.graph = G
            self.parent = [i for i in range(len(G))]
            for i in range(len(G)):
                for j in range(len(G)):
                    if G[i][j] != Graph.INF:
                        self.union(i, j)
        elif vertex > 0:
            self.graph = [[Graph.INF for j in range(vertex)] for i in range(vertex)]
            self.parent = [i for i in range(vertex)]

        self.vertex = len(self.graph)

    def push_edge(self, u, v, w):
        self.graph[u][v] = w

    def find(self, i):
        while self.parent[i] != i:
            i = self.parent[i]
        return i

    def union(self, i, j):
        a = self.find(i)
        b = self.find(j)
        self.parent[a] = b

    def Kruskal(self):
        V = self.vertex
        result = []
        mincost = 0  # Cost of min MST
        # Initialize sets of disjoint sets
        for i in range(V):
            self.parent[i] = i
        
        print("Start Kruskal")
        # Include minimum weight edges one by one
        edge_count = 0
        while edge_count < V - 1:
            min = Graph.INF
            a = -1
            b = -1
            for i in range(V):
                for j in range(V):
                    if self.find(i) != self.find(j) and self.graph[i][j] < min:
                        min = self.graph[i][j]
                        a = i
                        b = j
            if min != Graph.INF:
                self.union(a, b)
                print("Edge {}:({}, {}) cost:{}".format(edge_count, a, b, min))
                result.append([a, b, min])
                mincost += min
            edge_count += 1

        print("Finish Kruskal")
        print("Minimum cost= {}".format(mincost))
        return result, mincost