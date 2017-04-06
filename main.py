#!/usr/bin/env python3

import cv2, binascii, struct

def loadVideo(video):
    capture = cv2.VideoCapture(video)
    return capture

def getVideoDimensions(capture):
    '''Return the video dimensions as a tuple -> (h, w)'''
    success, frame = capture.read()
    return frame[:2]


def formatInput(input):
    '''Format string input so it can be written to the GIF file
        input should be an int
    '''
    return (input).to_bytes(2, byteorder='little')


t   

def createGif(height, width):
    # Create a GIF file with the GIF89a specification
    with open("small.gif", 'wb') as f:
        f.write(b'GIF89a') # Header Block
        height = formatInput(height)
        width = formatInput(width)
        f.write(height + width + b'\xF7\x00\x00') # Logical Screen Descriptor
        # Built Global Colour Table, have to iterate through each frame and create a dictionary entry for each
        # colour not encountered
        f.write(b'\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\x00\x00\x00') # Global Colour Table
        f.write(b'\x21\xF9\x04\x00\x00\x00\x00\x00') # Graphics Control Extension
        f.write(b'\x2C\x00\x00\x00\x00\x0A\x00\x0A\x00\x00') # Image Descriptor
        f.write(b'\x02\x16\x8C\x2D\x99\x87\x2A\x1C\xDC\x33\xA0\x02\x75\xEC\x95\xFA\xA8\xDE\x60\x8C\x04\x91\x4c\x01\x00') # Image Data
        f.write(b'\x3B') # Trailer (always b'\x3B')






if __name__ == "__main__":
    createGif(320, 560)