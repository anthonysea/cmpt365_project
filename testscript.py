import PIL
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata
import numpy as np
import os
import cv2

os.chdir("C:/Users/Anthony/Desktop")
im = Image.open("test.png").convert("P", palette=Image.ADAPTIVE, dither=1)
headerdata = getheader(im, palette=im.palette.palette)
print("data: ", headerdata)
print("\theader: ", headerdata[0])
print("\tpalette: ", headerdata[1])
print("palette: ", im.palette.palette)
print("\tpalette length: ", len(im.palette.tobytes()))

print(getdata(im))

def test1():
    video = cv2.VideoCapture("small.mp4")
    success, frame = video.read()
    count = 0
    images = []
    palettes, occur = [], []
    while success:
        im = Image.fromarray(frame, "RGB").convert("P", palette=Image.ADAPTIVE)
        #print(im.getpalette())
        images.append(im)
        #print(im.palette.palette)
        success, frame = video.read()
        count += 1
    print(count)

    for image in images:
        palettes.append(image.palette.palette)
    for palette in palettes:
        occur.append(palettes.count(palette))

    print("occur: ", len(occur))
