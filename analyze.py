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
    return np.array([v[key][component] for v in data if key in v])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for key in (str(i) for i in range(8)):
    data = extract(indata['data'], key, 'transform')
    x, y, z = data.T
    ax.plot(x, y, z, label=key)

ax.legend()
plt.savefig(args.output)
