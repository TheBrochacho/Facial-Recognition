import cv2
import numpy as np
import imutils


#used segments from this code
#https://github.com/informramiz/Face-Detection-OpenCV/blob/master/Face-Detection.py

haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
lbp_face_cascade = cv2.CascadeClassifier('data/lbpcascade_frontalface.xml')

def detect_faces(f_cascade, colored_img, scaleFactor = 1.1):
    	img_copy = np.copy(colored_img)
    	#convert the test image to gray image as opencv face detector expects gray images
    	gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    
    	#let's detect multiscale (some images may be closer to camera than others) images
    	faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);
    
    	#go over list of faces and draw them as rectangles on original colored img
    	for (x, y, w, h) in faces:
    		cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    	return img_copy

cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !appsink")

#cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)2592, height=(int)1944, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !appsink")

#cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !appsink")

while True:
	re, img = cap.read()

	#faces = detect_faces(haar_face_cascade, img)
	img = imutils.resize(img, width=800)
	
	cv2.imshow('camera', img)
	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyAllWindows()
		break
