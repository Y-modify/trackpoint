import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
import json

parser = argparse.ArgumentParser(description='Analyze the output data')
parser.add_argument('-i', '--input', type=str, required=True, help='Input json data')
parser.add_argument('-o', '--output', type=str, required=True, help='Output image path')

args = parser.parse_args()

with open(args.input) as f:
    indata = json.load(f)

metadata = indata['metadata']

def extract(data, key, component):
    return np.array([v[key][component] if key in v else [0, 0, 0] for v in data])

data = extract(indata['data'], '0', 'transform')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i, d in enumerate(data):
    if i == len(data) - 1:
        break

    X, Y, Z = d
    U, V, W = data[i + 1] - d
    ax.quiver(X, Y, Z, U, V, W)

plt.savefig(args.output)
