import numpy as np
import argparse
import json

parser = argparse.ArgumentParser(description='Plot the output data')
parser.add_argument('-i', '--input', type=str, required=True, help='Input json data')
parser.add_argument('-v', '--visualize', action="store_true", help='Show matplotlib window')
parser.add_argument('--dpi', type=int, default=400, help='DPI of output image')
parser.add_argument('--with-rotation', action="store_true", help='Add rotation arrows')
parser.add_argument('-s', '--smoothing', type=int, help='Take a moving average')
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
    def moving_average(a, n):
        a = np.ma.masked_array(a, np.isnan(a))
        ret = np.cumsum(a.filled(0), axis=0)
        ret[n:] = ret[n:] - ret[:-n]
        counts = np.cumsum(~a.mask, axis=0)
        counts[n:] = counts[n:] - counts[:-n]
        ret[~a.mask] /= counts[~a.mask]
        ret[a.mask] = np.nan
        return ret

    data = extract(indata['data'], key, 'transform')
    x, y, z = moving_average(data, args.smoothing).T if args.smoothing else data.T
    ax.plot(x, y, z, label=key)
    if args.with_rotation:
        rotation = extract(indata['data'], key, 'rotation')
        u, v, w = (rotation * data).T
        ax.quiver(x, y, z, u, v, w, length=0.05, normalize=True, label=key)

ax.legend()
plt.savefig(args.output, dpi=args.dpi)
if args.visualize:
    plt.show()
