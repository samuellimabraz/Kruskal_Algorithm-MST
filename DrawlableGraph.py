from Graph import Graph
from random import uniform, randint
from math import sqrt

# Classe derivada de Graph, contem uma lista de coordenadas para os vetices,
# e métodos para desenhar, representar o grafo em uma imagem
class DrawlableGraph(Graph):
    def __init__(self, graph=None, vertex=0, coordinates=None, height=1920, width=1080):
        super().__init__(graph, vertex)

        self.coordinates = []
        if coordinates:
            self.coordinates = coordinates

        self.height = height
        self.width = width

    def randomInit(self, vertex, vdist, edist, grau):
        super().__init__(vertex=vertex)
        # Gera lista de coordenadas aleatorias para os vértices
        self.randomCoordinates(vdist)
        # Gera lista de arestas com distancia minima
        self.randomEdges(edist)

    def randomCoordinates(self, vdist=100.0):
        # Gera lista de coordenadas aleatorias para os vértices
        # com uma distancia minima entre todos
        vertices = self.coordinates
        while len(vertices) < self.vertex:
            x = uniform(0, self.width)
            y = uniform(0, self.height)

            # Verificar se a nova posição é válida
            valido = True
            for i in vertices:
                dx = x - i[0]
                dy = y - i[1]

                if sqrt(dx**2 + dy**2) < vdist:
                    valido = False
                    break
            if valido:
                vertices.append([x, y])

    def randomEdges(self, edist=200.0, grau=3):
        # Gera lista de arestas com uma distancia minima e um grau máximo
        vertices = self.coordinates
        for i in range(len(vertices)):
            c = 0
            n = randint(3, grau)
            for j in range(i + 1, len(vertices)):
                dx = vertices[i][0] - vertices[j][0]
                dy = vertices[i][1] - vertices[j][1]

                distancia = sqrt(dx**2 + dy**2)
                if distancia < edist and c <= n:
                    self.push_edge(i, j, distancia)
                    c += 1

    def drawVertex(self, i, draw, color="black", vertex_width=2):
        x, y = self.coordinates[i]
        draw.ellipse(
            (x - 4.2, y - 4.2, x + 4.2, y + 4.2), fill=color, width=vertex_width
        )

    def drawEdge(self, i, j, draw, color="gray", edge_width=1):
        if self.graph[i][j] != Graph.INF:
            xi, yi = self.coordinates[i]
            xj, yj = self.coordinates[j]
            draw.line((xi, yi, xj, yj), fill=color, width=edge_width)

    def drawGraph(
        self, draw, vcolor="black", ecolor="gray", vertex_width=1, edge_width=1
    ):
        for i in range(self.vertex):
            self.drawVertex(i, draw, vcolor, vertex_width)
        for i in range(self.vertex):
            for j in range(self.vertex):
                self.drawEdge(i, j, draw, ecolor, edge_width)