import numpy as np

# Define conversions in x and y from pixels space to meters
ym_per_pix = 30/720 # meters per pixel in y dimension
xm_per_pix = 3.7/700 # meters per pixel in x dimension
	
def measure(ploty, leftx, rightx):
	'''
	Calculates the curvature of polynomial functions in meters.
	'''

	left_fit_cr = np.polyfit(ploty*ym_per_pix, leftx*xm_per_pix, 2)
	right_fit_cr = np.polyfit(ploty*ym_per_pix, rightx*xm_per_pix, 2)

	# Define y-value where we want radius of curvature
	# We'll choose the maximum y-value, corresponding to the bottom of the image
	y_eval = np.max(ploty)

	##### Implement the calculation of R_curve (radius of curvature) #####
	left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
	right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])

	return left_curverad, right_curverad
	
	
def distance(image, left_fitx, right_fitx):
	# get the center of the image
	image_size_x = image.shape[1]

	# get the last values of x from left and right
	left_x = left_fitx[-1]
	right_x = right_fitx[-1]
	
	# compute the value of the center of the lane
	center_x = left_x + ((right_x - left_x) / 2)

	# compute the offset and ocnvert it to meters
	offset = ((image_size_x / 2) - center_x) * xm_per_pix

	return offset