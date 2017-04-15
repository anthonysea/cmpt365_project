import PIL
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata
import cv2
import numpy as np


def intToBin(i):
    """ Format the integer to binary as two bytes.
        i should be an int. """
    return (i).to_bytes(2, byteorder="little")


def getVideoFrames(filepath):
    """ Get the frames of the video and return a list of Image objects.
        file path should be a string of the path to the video file. """
    video = cv2.VideoCapture(filepath)
    frames = []
    success, frame = video.read()  # Read the first frame

    while success:
        frame = Image.fromarray(frame, "RGB")
        b, g, r = frame.split()  # Convert BGR to RGB
        frame = Image.merge("RGB", (r, g, b))
        frame.thumbnail((300, 300))  # Resize frame
        frame = frame.convert("P", palette=Image.ADAPTIVE)

        frames.append(frame)
        success, frame = video.read()

    return frames


def getHeader(img):
    """ Return the line for the Header Block and the Logical Screen Descriptor. Uses the first
        frame to get the img width and img height. """
    line = b"GIF89a"  # Specify GIF89a standard
    line += intToBin(img.size[0])
    line += intToBin(img.size[1])
    line += b"\x87\x00\x00"  # \x87 = packed field
    return line


def getGfxCtrlExt():
    """ Graphics Control Extension Block. """
    line = b"\x21\xF9\x04"  # \x21 = Extension introducer, \xF9 = Graphics control label, \x04 = Byte size
    line += b"\x00"  # Transparency; set to false
    line += intToBin(10)  # Delay time
    line += b"\x00"  # Transparent colour; set to false
    line += b"\x00"  # Block terminator
    return line

def getImgDesc(img):
    """ Image Descriptor Block. """
    line = b"\x2C"  # Image separator
    line += b"\x00\x00"  # Image left position
    line += b"\x00\x00"  # Image top position
    line += intToBin(img.size[0])
    line += intToBin(img.size[1])
    line += b"\x87"  # Packed field (10000111)
    return line


def getAppExt():
    """ Application Extension Block. """
    line = b"\x21\xFF\x0B"  # Specifies the application extension block
    line += b"NETSCAPE2.0"
    line += b"\x03\x01\x00\x80"  # \x03 = length of data sub-block, \x00\x80 = number of loops that should be executed
    line += b"\x00"  # Data sub-block terminator
    return line


def writeToFile(fp, images):
    """ Writes the set of images to a GIF fp. """

    palettes, count = [], []
    for img in images:
        palettes.append(img.palette.palette)
    for pal in palettes:
        count.append(palettes.count(pal))

    gct = palettes[count.index(max(count))]

    frames = 0
    firstFrame = True

    for img, pal in zip(images, palettes):

        if firstFrame:

            header = getHeader(img)
            gce = getGfxCtrlExt()
            appExt = getAppExt()

            fp.write(header)
            fp.write(gct)
            fp.write(appExt)

            firstFrame = False

        if True:

            data = getdata(img)
            print(data)
            imgDes, data = data[0], data[1:]
            gce = getGfxCtrlExt()
            localImgDes = getImgDesc(img)

            if pal != gct:
                fp.write(gce)
                fp.write(localImgDes)
                fp.write(pal)
                # fp.write(b"\x08")  # LZW min code size (included in getdata())
            else:
                fp.write(gce)
                fp.write(imgDes)


            for d in data:
                fp.write(d)

        frames = frames + 1

    fp.write(b"\x3B")
    return frames

if __name__ == "__main__":
    fp = open("out.gif", "wb")
    frames = getVideoFrames("C:/Users/Anthony/Desktop/10.mp4")
    print(writeToFile(fp, frames))





