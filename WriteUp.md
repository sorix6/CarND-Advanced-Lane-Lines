
### Advanced Lane Finding Project

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.



#### Camera Calibration

The camera calibration code can be found in the file calibration.py
While using the images provided in the camera_cal folder I have taken the following steps:
1. Each image has been converted to grayscale 
2. Found the chessboard corners using the cv2.findChessboardCorners() function
3. Found the calibration parameteres of the camera by using the information retrieved in step 2 and the cv2.calibrateCamera() function
4. Saved the calibration parameters in the file data_exports/calibration.p

By using the calibration parameters and the cv2.undistort() function, I have come to the following results:

Original image | Corner detection | Undistorted image  
------------ | ------------- | ------------- 
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/camera_cal/calibration2.jpg) | ![carners image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/corners_calibration2.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_calibration2.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/camera_cal/calibration9.jpg) | ![carners image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/corners_calibration9.jpg) | ![originalundistortedcarners](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_calibration9.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/camera_cal/calibration13.jpg) | ![carners image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/corners_calibration13.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_calibration13.jpg)


#### Pipeline (single images)

By using the calibration parameters from the file data_exports/calibration.p, I came to the following results:

Original image | Undistorted image  
------------ | -------------
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/straight_lines1.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_straight_lines1.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/straight_lines2.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_straight_lines2.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/test1.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_test1.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/test2.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_test2.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/test3.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_test3.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/test4.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_test4.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/test5.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_test5.jpg)
![original image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/test_images/test6.jpg) | ![undistorted image](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/outputs/undist_test6.jpg)


In order to create a thresholded binary image, I have created the function my_pipeline() in the file gradient_color.py. The function contains the following steps:
1. Converting to the HLS color space and separating the V channel
2. Applying a Sobel operator on x and compute the absolute x derivate
3. Create a threshold gradient on x
4. Create a color channel threshold
5. Stach the results of step 3. and step 4. in order to return the result


The code for my perspective transform is available in iPython notebook. The parameters are defined in cell 2 and in cell 10, at line 10, the cv2.warpPerspective() function is called.

I chose to hardcode the source and destination points in the following manner:

```python
src = np.float32([[[ 610,  450]], 
                      [[ 680,  450]], 
                      [[ img_size[0]-300,  680]],
                      [[ 380,  680]]])

# Result points        
dst = np.float32([[offset, 0], 
                [img_size[0]-offset, 0], 
                [img_size[0]-offset, img_size[1]], 
                [offset, img_size[1]]])

```

The parameter img_size contains the x and y dimensions of the first image in the batch of images.

![result images](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/output_images/undistorted_color_warped.JPG)


The methods used in the process of lane-line pixels are contained in the fole lane_detect.py.

The first step was to display the histogram for the input images:

![histogram images](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/output_images/histograms.jpg)


##### The method  find_lane_pixels:
* Parameters
Sliding windows: 9
Width of the windows +/- margin: 100
Minimum number of pixels found to recenter window: 50
  
1. Take a histogram of the bottom half of the image
2. Create an output image to draw on and visualize the result
3. Find the peak of the left and right halves of the histogram
4. Set height of windows - based on nwindows above and image shape
5. Identify the x and y positions of all nonzero pixels in the image
6. Step through the windows one by on, identify the nonzero pixels in x and y within the window and draw the windows on the visualization image
7. Extract left and right line pixel positions and fit a second order polynomial to each using np.polyfit()
8. Generate the values of x and y needed for plotting

##### The method search_around_poly:
* Parameters
Margin: 100

1. Grab activated pixels
2. Set the area of search based on activated x-values within the +/- margin of the polynomial function
3. Extract left and right line pixel positions
4. Fit new polynomials
5. Draw the image with the relevant new information

![lanes](https://raw.githubusercontent.com/sorix6/CarND-Advanced-Lane-Lines/master/output_images/window_lanes.JPG)


The curvatures have been calculated using the method measure() from the file curvature.py. The curvature information has been displayed on the same image that displayes the detected lane.

---

### Pipeline (video)

The result of applying the pipeline to the video project_video.mp4 can be found in the folder video_results.

### Discussion

The pipeline does not perform very well on the two challenge videos. More tunning is in need in order to fix this issue. 
The problems seem to appear due to the different colors of the pavement. Changes in the method that generates the thresholded binary should improve the results.