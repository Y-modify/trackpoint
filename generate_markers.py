from cv2 import aruco
import sys
from PIL import Image, ImageDraw
import math
import argparse

parser = argparse.ArgumentParser(description='Generate an image containing ArUco markers')
parser.add_argument('-n', '--num', type=int, required=True, help='The number of markers')
parser.add_argument('-s', '--size', type=int, default=100, help='The side length of markers')
parser.add_argument('-p', '--padding', type=int, default=10, help='The padding between markers')
parser.add_argument('-r', '--rows', type=int, default=4, help='The number of markers in one row')
parser.add_argument('-o', '--out', type=str, required=True, help='Output Image')
parser.add_argument('-l', '--with-label', action="store_true", help='Print labels in output image')
parser.add_argument('--dict', type=str, default="4X4_50", help='The ArUco marker dictionary')
args = parser.parse_args()

num = args.num
size = args.size
padding = args.padding
rows = args.rows
cols = math.ceil(num / rows)

length = size + 2 * padding
canvas = Image.new('L', (length * rows, length * cols), 255)
draw = ImageDraw.Draw(canvas)

dictionary = aruco.getPredefinedDictionary(getattr(aruco, "DICT_" + args.dict))

for i in range(num):
    marker = aruco.drawMarker(dictionary, i, size)
    image = Image.fromarray(marker, mode='L')
    x_pos = (i % rows) * length + padding
    y_pos = (i // rows) * length + padding
    canvas.paste(image, (x_pos, y_pos))
    if args.with_label:
        x_text_pos = x_pos + length / 2
        y_text_pos = y_pos + length - padding * 2
        draw.text((x_text_pos, y_text_pos), str(i), fill=0)

canvas.save(args.out)
