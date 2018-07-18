from cv2 import aruco
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Generate an image containing ArUco markers')
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--input', type=str, help='Input Movie')
group.add_argument('-c', '--camera', type=int, default=0, help='Input Camera')
parser.add_argument('--dict', type=str, default="4X4_50", help='The ArUco marker dictionary used in the movie')
parser.add_argument('-m', '--camera-matrix', type=str, required=True, help='THe path to npy file contains the camera matrix')
parser.add_argument('-d', '--dist-coeff', type=str, required=True, help='THe path to npy file contains the distortion coefficients')

args = parser.parse_args()

dictionary = aruco.getPredefinedDictionary(getattr(aruco, "DICT_" + args.dict))

cameraMatrix = np.load(args.camera_matrix)
distCoeff = np.load(args.dist_coeff)

result = []

cap = cv2.VideoCapture(args.input if args.input else args.camera)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, _ = aruco.detectMarkers(gray, dictionary, cameraMatrix=cameraMatrix, distCoeff=distCoeff)

    result.append({int(idn): corner.tolist() for (corner, idn) in zip(corners, ids)})

cap.release()
cv2.destroyAllWindows()

print(result)
