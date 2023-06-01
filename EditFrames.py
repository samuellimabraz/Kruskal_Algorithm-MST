from PIL import Image, ImageDraw, ImageFont

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