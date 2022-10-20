import cv2
import numpy as np
import matplotlib.pyplot as plt


frameWidth= 640         # CAMERA RESOLUTION
frameHeight = 480
brightness = 180

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, brightness)


# def preprocessing(img,img2):
#     lane_canny = finding_canny(img)
#     cropped_canny = region_focus(lane_canny)
#     lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
#     averaged_lines = average_slope_intercept(img2, lines)
#     line_image = show_lines(img, lines)
#     combo_image = cv2.addWeighted(img, 0.8, line_image, 1, 1)
#     #img = img/255
#     return img

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
    # blur_application = cv2.GaussianBlur(gray_image, (5,5), 0)
    canny = cv2.Canny(gray_image, 50 ,150)  # extract the rapid changing in the gradient color of the image
    return canny

def region_focus(img):
    height = img.shape[0]
    triangle = np.array([
        [(100, height ), (900,height), (500, 300)]
        ])
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


# image = cv2.imread('lane.jpeg')
# lane_image = np.copy(image)
# lane_canny = finding_canny(lane_image)
# cropped_canny = region_focus(lane_canny)
# lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
# averaged_lines = average_slope_intercept(image, lines)
# line_image = show_lines(lane_image, lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# cv2.imshow('result', combo_image)
# cv2.waitKey(0)


while(True):
    success, imgOrignal = cap.read()
 
# PROCESS IMAGE
    image = np.asarray(imgOrignal)
    lane_image = np.copy(image)
    
    lane_canny = finding_canny(lane_image)
    cropped_canny = region_focus(lane_canny)
    lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
    # averaged_lines = average_slope_intercept(image, lines)
    line_image = show_lines(lane_image, lines)
    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    cv2.imshow("Processed Image", combo_image)
    if cv2.waitKey(1) and 0xFF == ord('q'):
       break




# cap = cv2.VideoCapture(0)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# cap.set(10, brightness)

# i=0
# while (cap.isOpened()):
#     if i%5==0:
#                         frame = cap.read()   

#                         lane_canny = finding_canny(frame)
#                         cropped_canny = region_focus(lane_canny)
#                         lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
#                         averaged_lines = average_slope_intercept(frame, lines)
#                         line_image = show_lines(frame, lines)
#                         combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
#                         cv2.imshow("result", combo_image)
#                         if cv2.waitKey(10)& 0xFF == ord('q'):
#                             break;
# cap.release()
# cv2.destroyAllWindows()

# plt.imshow(lane_canny)
# plt.show()

# cap = cv2.VideoCapture('test2.mp4')

# while(cap.isOpened()):

#     _, frame = cap.read()
#     canny = finding_canny(frame)
#     selected_region = region_focus(canny)
#     finding_lines = cv2.HoughLinesP(selected_region, 2 , np.pi/180, 100, np.array([]), minLineLength=40 , maxLineGap=50)
#     average = average_slope_intercept(frame, finding_lines)
#     line_image = show_lines(frame,average)
#     merge_image = cv2.addWeighted(frame, 0.8, line_image , 1, 1)
#     cv2.imshow('result',merge_image)
#     cv2.waitKey(1)