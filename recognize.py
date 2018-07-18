from cv2 import aruco
import cv2
import numpy as np
import argparse
import json

parser = argparse.ArgumentParser(description='Generate an image containing ArUco markers')
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--input', type=str, help='Input Movie')
group.add_argument('-c', '--camera', type=int, default=0, help='Input Camera')
parser.add_argument('--dict', type=str, default="4X4_50", help='The ArUco marker dictionary used in the movie')
parser.add_argument('-m', '--camera-matrix', type=str, required=True, help='The path to npy file contains the camera matrix')
parser.add_argument('-d', '--dist-coeff', type=str, required=True, help='The path to npy file contains the distortion coefficients')
parser.add_argument('-s', '--size', type=float, required=True, help='The length of the markers\' side')
parser.add_argument('-o', '--output', type=str, help='Output path')
parser.add_argument('--output-video', type=str, help='Output the processes video to the specified path')
parser.add_argument('--output-codec', type=str, default='XVID', help='The fourcc code to output the video')

args = parser.parse_args()

dictionary = aruco.getPredefinedDictionary(getattr(aruco, "DICT_" + args.dict))

cameraMatrix = np.load(args.camera_matrix)
distCoeff = np.load(args.dist_coeff)

result = []

cap = cv2.VideoCapture(args.input if args.input else args.camera)
ret, frame = cap.read()
height, width, _ = frame.shape
fps = cap.get(cv2.CAP_PROP_FPS)

if args.output_video:
    fourcc = cv2.VideoWriter_fourcc(*args.output_codec)
    out = cv2.VideoWriter(args.output_video, fourcc, fps, (width, height))

while ret:
    corners, ids, _ = aruco.detectMarkers(frame, dictionary, cameraMatrix=cameraMatrix, distCoeff=distCoeff)

    rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, args.size, cameraMatrix, distCoeff)

    result.append({int(idn): {"rotation": rvec[0].tolist(), "transform": tvec[0].tolist()} for (rvec, tvec, idn) in zip(rvecs, tvecs, ids)})

    if args.output_video:
        aruco.drawDetectedMarkers(frame, corners, ids, (0,255,0))
        for rvec, tvec in zip(rvecs, tvecs):
            aruco.drawAxis(frame, cameraMatrix, distCoeff, rvec, tvec, 0.1)
        out.write(frame)

    ret, frame = cap.read()

cap.release()
if args.output_video:
    out.release()
cv2.destroyAllWindows()

if args.output:
    with open(args.output, 'w') as f:
        json.dump(result, f)
else:
    print(json.dumps(result))
