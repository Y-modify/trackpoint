import numpy as np
import argparse
import json

parser = argparse.ArgumentParser(description='Analyze the output data')
parser.add_argument('-i', '--input', type=str, required=True, help='Input json data')
parser.add_argument('-v', '--visualize', action="store_true", help='Show matplotlib window')
parser.add_argument('--dpi', type=int, default=400, help='DPI of output image')
parser.add_argument('-o', '--output', type=str, required=True, help='Output image path')

args = parser.parse_args()

if not args.visualize:
    import matplotlib as mpl
    mpl.use('Agg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

with open(args.input) as f:
    indata = json.load(f)

metadata = indata['metadata']

def extract(data, key, component):
    return np.array([v[key][component] if key in v else [np.nan]*3 for v in data])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for key in (str(i) for i in range(8)):
    data = extract(indata['data'], key, 'transform')
    x, y, z = data.T
    ax.plot(x, y, z, label=key)
    rotation = extract(indata['data'], key, 'rotation')
    u, v, w = (rotation * data).T
    ax.quiver(x, y, z, u, v, w, length=0.05, normalize=True)

ax.legend()
plt.savefig(args.output, dpi=args.dpi)
if args.visualize:
    plt.show()
