import cv2
import os
from moviepy.editor import *

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