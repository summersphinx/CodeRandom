from PIL import Image
import os

import numpy as np

for image in os.listdir(os.getcwd() + '/Reddit/'):
    img = Image.open(os.getcwd() + '/Reddit/' + image)
    width = img.size[0]
    height = img.size[1]
    for i in range(0, width):  # process all pixels
        for j in range(0, height):
            data = img.getpixel((i, j))
            if data[0] == 0 and data[1] == 0 and data[2] == 0 and data[3] == 255:
                img.putpixel((i, j), (255, 215, 0))
    img.save(os.getcwd() + '/Python/' + image)

