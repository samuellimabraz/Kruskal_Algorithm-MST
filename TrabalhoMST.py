from random import uniform, randint
from math import sqrt
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import ffmpeg
from moviepy.editor import *


# Classe representando um grfo por matriz de adjacencia, e métodos para o algoritmo de Kruskal
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


# Função auxiliar para escrever um texto temporario sobre uma imagem
def textOnImage(img, xy, text, font, txt_color, path, arq):
    width, height = img.size
    txt = Image.new("RGBA", (width, height))
    aux = Image.new("RGBA", (width, height))
    draw_txt = ImageDraw.Draw(txt)

    draw_txt.text(
        xy=xy,
        text=text,
        fill=txt_color,
        font=ImageFont.truetype(font[0], font[1]),
        align="center",
    )
    aux = Image.alpha_composite(img, txt)
    aux.save(rf"{path}\{arq}")


def createFrames(
    start_frame,
    final_frame,
    font,
    txt_color,
    path,
    img=None,
    size=(1080, 1920),
    bg_color="white",
    xy=(540, 960),
    text="",
):
    if img == None:
        img = Image.new("RGBA", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    draw.text(
        xy=xy,
        text=text,
        fill=txt_color,
        font=ImageFont.truetype(font[0], font[1]),
        align="center",
    )
    for i in range(start_frame, final_frame):
        img.save(rf"{path}\{i}.png")
        print(f"{i}.png")


def kruskalFrames(dgraph, result, mincost, font, colors, frame, path):
    print(f"Creating Kruskal frames G({dgraph.vertex})...")

    # Cria uma imagem com fundo colorido
    img = Image.new("RGBA", (dgraph.width, dgraph.height), color=colors["blue"])
    draw_img = ImageDraw.Draw(img)

    # Desenha todo o Grafo
    dgraph.drawGraph(draw_img, vcolor=colors["white"], ecolor=colors["gray"])
    img.save(rf"{path}\{frame}.png")
    print(f"{frame}.png")

    # Desenha o percurso da MST gerada pelo Kruskal
    dist = 0
    for i in range(len(result)):
        u, v, d = result[i]
        dist += d
        frame += 1
        dgraph.drawEdge(u, v, draw_img, colors["yellow_1"], 4)
        textOnImage(
            img=img,
            xy=(400, 1600),
            text=f"({u}, {v}) cost: {d:.2f}\nMin_cost: {dist:.2f}",
            font=font,
            txt_color=colors["black"],
            path=path,
            arq=f"{frame}.png",
        )
        print(f"{frame}.png")
    frame += 1
    # Cria frames com o resultado final para 0.75 segundos
    createFrames(
        start_frame=frame,
        final_frame=frame + 75,
        font=font,
        txt_color=colors["black"],
        path=path,
        img=img,
        text=f"Min cost: {mincost:.2f}",
        xy=(300, 700),
    )
    print(f"Finish Kruskal frames G({dgraph.vertex})")
    return img


def createVideo(duration, video_path, frames_path):
    print("Creating video...")

    images = [img for img in os.listdir(frames_path) if img.endswith(".png")]
    images.sort()
    num_frames = len(images)
    fps = num_frames / duration
    print(f"fps = {fps}")

    frame = cv2.imread(os.path.join(frames_path, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(video_path, fourcc, float(fps), (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(frames_path, image)))

    cv2.destroyAllWindows()
    video.release()

    print("Finish video")


def addAudio(audio_path, video_path, output_path):
    print("Adding Audio...")

    audio = AudioFileClip(audio_path)
    video = VideoFileClip(video_path)

    audio = audio.subclip(8, video.duration+8)

    # Adiciona o áudio cortado ao vídeo
    video_final = video.set_audio(audio)

    # Extrai o vídeo de saída final
    video_final.write_videofile(output_path)

    print("Finish Audio")


def main():
    # Diretorios e recursos
    path = r"D:\Samuel\UNIFEI\3_Semestre\Grafos\Trabalho"
    frames_path = rf"{path}\frames"
    os.mkdir(frames_path)

    video_path = rf"{path}\video.mp4"
    video_audio_path = rf"{path}\video_audio.mp4"
    output_final_path = rf"{path}\video_final.mp4"

    gif_intro_path = r"C:\Users\humbr\Downloads\club_penguin_dance.mp4"
    gif_final_path = r"C:\Users\humbr\Downloads\club_penguin_break_dance.mp4"
    audio_path = r"C:\Users\humbr\Downloads\Uptown_Funk_sax.mp4"

    font = rf"C:\Users\humbr\Downloads\amatic_sc_bold.ttf"

    # Parametros gerais
    height, width = 1920, 1080
    video_duration = 30
    intro_duration = time = 2.5
    final_duration = 1.5
    fps = 100
    colors = {
        "blue": (20, 125, 255, 255),
        "white": (255, 255, 255, 255),
        "black": (0, 0, 0, 255),
        "gray": (245, 238, 224, 255),
        "yellow_1": (255, 255, 0, 255),
        "yellow_2": (255, 219, 75, 255),
    }
    graph_parameters = [
        [100, 100.0, 200.0, 4],
        [400, 60.0, 200.0, 3],
        [800, 40.0, 150.0, 3],
        [1000, 20.0, 130.0, 3],
    ]
    frame = 1000

    clips = []
    aux = []

    # Cria frames para introdução de 5 segundos
    print("Creating introduction frames...")
    createFrames(
        start_frame=frame,
        final_frame=int((fps * intro_duration) + frame),
        size=(width, height),
        bg_color=colors["yellow_2"],
        xy=(360, 700),
        text="Algoritmo\nde\nKruskal",
        font=[font, 120],
        txt_color=colors["blue"],
        path=frames_path,
    )
    frame += int((fps * intro_duration))

    print("Finish introduction frames")

    # Gera um "Grafo desenhavel" para uma imagem 1920x1080
    G = DrawlableGraph(height=height, width=width)

    for vertex, vdist, edist, grau in graph_parameters:
        print(f"Start G({vertex})...")

        # Inicia com as coordenadas dos vertices aleatorias, e arestas com distancia maxima
        G.randomInit(vertex=vertex, vdist=vdist, edist=edist, grau=grau)

        # Realiza o Kruskal e recebe a lista do caminho percorrido e o custo total minimo
        result, mincost = G.Kruskal()

        # Criação dos frames da rota do Kruskal
        kruskalFrames(
            dgraph=G,
            result=result,
            mincost=mincost,
            font=[font, 98],
            colors=colors,
            frame=frame,
            path=frames_path,
        )
        aux.append(
            TextClip(
                txt=f"Vertex = {vertex}",
                size=(width, height),
                fontsize=100,
                color="white",
                font="Open-Sans-Bold-Italic",
            )
            .set_position("center")
            .set_start(time)
            .set_duration(1)
            .crossfadein(0.75)
        )
        time += (vertex + 75) / fps
        frame += vertex + 75
        print(f"Finish G({vertex})\n")

    # Cria frames para final de 2 segundos
    print("\nCreating final frames...")
    createFrames(
        start_frame=frame,
        final_frame=int((fps * final_duration) + frame),
        size=(width, height),
        xy=(400, 800),
        bg_color=colors["yellow_2"],
        text="Obrigado",
        font=[font, 120],
        txt_color=colors["blue"],
        path=frames_path,
    )
    print("Finish final frames")

    # Cria vídeo unindo todos os frames
    createVideo(
        duration=video_duration,
        video_path=video_path,
        frames_path=frames_path,
    )

    addAudio(audio_path, video_path, video_audio_path)

    print("Editing video...")
    clips.append(VideoFileClip(video_audio_path))
    clips.append(
        VideoFileClip(gif_intro_path)
        .set_start(0)
        .set_duration(intro_duration)
        .set_position(("center", 1140))
    )
    clips.extend(aux)
    clips.append(
        VideoFileClip(gif_final_path)
        .set_start(video_duration - final_duration)
        .set_duration(video_duration)
        .set_position(("center", 1140))
    )

    final = CompositeVideoClip(clips).set_duration(video_duration)
    final.write_videofile(output_final_path)
    print("Finish edit")


if __name__ == "__main__":
    main()
