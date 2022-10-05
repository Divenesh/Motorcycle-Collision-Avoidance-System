import cv2
import numpy as np
from scipy.stats import itemfreq
import matplotlib.pyplot as plt


def make_coordinates(img, line_parameters):
    slope, intercept = line_parameters
    y1 = img.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(img, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2), 1)
        slope =parameters[0]
        intercept =parameters [1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np. average(left_fit, axis=0)
    right_fit_average= np. average(right_fit, axis=0)
    left_line = make_coordinates(img, left_fit_average)
    right_line = make_coordinates(img, right_fit_average)
    return np.array([left_line, right_line])

def finding_canny(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #grayscalling image
    blur_application = cv2.GaussianBlur(gray_image, (5,5), 0)
    canny = cv2.Canny(blur_application, 50 ,150)  # extract the rapid changing in the gradient color of the image
    return canny

def region_focus(img):
    height = img.shape[0]
    triangle = np.array([[(200, height ), (1100,height), (550, 250)]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, triangle, 255)
    image_masked = cv2.bitwise_and(img,mask)
    return image_masked

def show_lines (img, lines):
    image_line = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(image_line, (x1,y1), (x2,y2), (255,0,0), 10)
    return image_line


#cv2.imshow('result',image)

# image = cv2.imread('test_image.jpg') #read and form number array
# image2 = np.copy(image)



# image = cv2.imread('test_image.jpg')
# lane_image = np.copy(image)
# lane_canny = finding_canny(lane_image)
# cropped_canny = region_focus(lane_canny)
# lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
# averaged_lines = average_slope_intercept(image, lines)
# line_image = show_lines(lane_image, averaged_lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 0)
# cv2.imshow('result',combo_image)
# cv2.waitKey(0)

cap = cv2.VideoCapture('test2.mp4')

while(cap.isOpened()):

    _, frame = cap.read()
    canny = finding_canny(frame)
    selected_region = region_focus(canny)
    finding_lines = cv2.HoughLinesP(selected_region, 2 , np.pi/180, 100, np.array([]), minLineLength=40 , maxLineGap=50)
    average = average_slope_intercept(frame, finding_lines)
    line_image = show_lines(frame,average)
    merge_image = cv2.addWeighted(frame, 0.8, line_image , 1, 1)
    cv2.imshow('result',merge_image)
    cv2.waitKey(1)