from PIL import Image, ImageDraw
from moviepy.editor import *
import os

from DrawlableGraph import DrawlableGraph
from Video import createVideo, addAudio
from EditFrames import createFrames, textOnImage

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
        # Adiciona texto com número de vertices
        # com efeito Fade in no inicio de cada grafo
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
