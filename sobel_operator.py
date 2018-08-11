import numpy as np
import cv2

def abs_sobel_thresh(gray, orient='x', thresh_min=0, thresh_max=255):
    x = 1
    y = 0
    
    if (orient == 'y'):
        y = 1
        x = 0
    
    
    # Take the derivative in x or y given orient = 'x' or 'y'
    sobel = cv2.Sobel(gray, cv2.CV_64F, x, y)
    # Take the absolute value of the derivative or gradient
    abs_sobel = np.absolute(sobel)
    # Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Create a mask of 1's where the scaled gradient magnitude 
            # is > thresh_min and < thresh_max
            
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    
    return binary_output

def mag_thresh(gray, sobel_kernel=3, mag_thresh=(0, 255)):
	
    # Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
	
    # Calculate the magnitude 
    gradmag = np.sqrt(sobelx**2 + sobely**2)
	
    # Scale to 8-bit (0 - 255) and convert to type = np.uint8
    scale_factor = np.max(gradmag)/255 
    gradmag = (gradmag/scale_factor).astype(np.uint8)
	
    # Create a binary mask where mag thresholds are met
    binary_output = np.zeros_like(gradmag)
    binary_output[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1
   
    return binary_output
    	
def dir_threshold(gray, sobel_kernel=3, thresh=(0, np.pi/2)):
	
    # Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
	
    # Take the absolute value of the x and y gradients
    # Use np.arctan2(abs_sobely, abs_sobelx) to calculate the direction of the gradient 
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
	
    # Create a binary mask where direction thresholds are met
    binary_output = np.zeros_like(absgraddir)
    binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1    

    return binary_output
	
def combine_thresholds(image):
	# Choose a Sobel kernel size
	ksize = 7 # Choose a larger odd number to smooth gradient measurements
	
	# Convert to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	
	# Apply each of the thresholding functions
	gradx = abs_sobel_thresh(gray, orient='x', thresh_min=10, thresh_max=160)
	grady = abs_sobel_thresh(gray, orient='y', thresh_min=10, thresh_max=160)
	mag_binary = mag_thresh(gray, sobel_kernel=ksize)
	dir_binary = dir_threshold(gray, sobel_kernel=ksize)
	
	combined = np.zeros_like(gradx)
	combined[ ((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1))] = 1
	
	return combined