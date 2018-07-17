from cv2 import aruco
import sys
from PIL import Image
import math

num = 16
size = 100
padding = 10
rows = 4
cols = math.ceil(num / rows)

length = size + 2 * padding
canvas = Image.new('L', (length * rows, length * cols), 255)

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

for i in range(num):
    marker = aruco.drawMarker(dictionary, i, size)
    image = Image.fromarray(marker, mode='L')
    x_pos = (i % rows) * length + padding
    y_pos = (i // rows) * length + padding
    canvas.paste(image, (x_pos, y_pos))

canvas.save("out.png")
