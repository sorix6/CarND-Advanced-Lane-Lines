import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import pickle

nx = 9
ny = 6
img_shape = (1280, 720)

def collect_points():
	objpoints = [] 									# 3D points in real world
	imgpoints = [] 									# 2D points in image plane
	
	# Prepare the object points
	objp = np.zeros((nx * ny, 3), np.float32)
	objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2) # x, y coordinates
	
	for f in os.listdir("camera_cal/"):
		img = mpimg.imread('./camera_cal/' + f);
		
		# Convert to grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		# Find the chessboard corners
		ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
		
		# If found, add object and image points
		if ret == True:
			imgpoints.append(corners)
			objpoints.append(objp)
			
			# Draw the detected corners on the image
			#img = cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
		
			#cv2.imwrite("outputs/corners_"+f, img)
				

	return objpoints, imgpoints
	
def calibrate_camera(objpoints, imgpoints):	
	# calibrate the camera using the points collected from all the images
	list = os.listdir("camera_cal/")
		
	image = mpimg.imread('./camera_cal/' + list[0])
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image.shape[0:2], None, None)
	
	return mtx,dist
	
	
objpoints, imgpoints = collect_points()
mtx, dist = calibrate_camera(objpoints, imgpoints)

# save the calibration data to file
data = {"camera_matrix": mtx, "distortion_coeff": dist}

file = open("./data_exports/calibration.p", "wb")
pickle.dump(data, file)
file.close()
