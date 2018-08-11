import cv2
import pickle

def undistort_image(img, mtx, dist):
	undist = cv2.undistort(img, mtx, dist, None, mtx)
	
	#cv2.imwrite("outputs/undist_"+f, undist)
	
	return undist

def getCalibrationParameters():
	
	# get the calibration data from file
	file = open("./data_exports/calibration.p", "rb")
	data = pickle.load(file)
	file.close()

	mtx = data['camera_matrix']
	dist = data['distortion_coeff']
	
	return mtx, dist


	
	