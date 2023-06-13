import numpy as np
import cv2
from keras.models import load_model
#############################################
 
frameWidth= 640         # CAMERA RESOLUTION
frameHeight = 480
brightness = 180
threshold = 0.95         # PROBABLITY THRESHOLD
font = cv2.FONT_HERSHEY_SIMPLEX
##############################################
 
# SETUP THE VIDEO CAMERA
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, brightness)
# IMPORT THE TRANNIED MODEL
model = load_model("modelnew.h5")
 
def grayscale(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img
def equalize(img):
    img =cv2.equalizeHist(img)
    return img
def preprocessing(img):
    img = grayscale(img)
    #img = equalize(img)
    img = img/255
    return img
def getCalssName(classNo):
    if   classNo == 0: return 'Speed Limit 30 km/h'
    elif classNo == 1: return 'Speed Limit 60 km/h'
    elif classNo == 2: return 'Speed Limit 120 km/h'

def region_focus(img):
    height = img.shape[0]
    triangle = np.array([
        [(100, height ), (900,height), (500, 300)]
        ])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, triangle, 255)
    image_masked = cv2.bitwise_and(img,mask)
    return image_masked
 
while True:
 
# READ IMAGE
    success, imgOrignal = cap.read()
 
# PROCESS IMAGE
    img = np.asarray(imgOrignal)
    img = cv2.resize(img, (32, 32))
    img = preprocessing(img)
    #img = region_focus(img)
    #cv2.imshow("Processed Image", img)
    img = img.reshape(1, 32, 32, 1)
    cv2.putText(imgOrignal, "CLASS: " , (20, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(imgOrignal, "PROBABILITY: ", (20, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
# PREDICT IMAGE
    predictions = model.predict(img)
    classIndex = np.argmax(predictions,axis=1)
    probabilityValue =np.amax(predictions)
    if probabilityValue > threshold:
        print(getCalssName(classIndex))
        cv2.putText(imgOrignal,str(classIndex)+" "+str(getCalssName(classIndex)), (120, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(imgOrignal, str(round(probabilityValue*100,2) )+"%", (180, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow("Result", imgOrignal)
 
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break