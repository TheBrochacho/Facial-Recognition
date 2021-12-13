import dlib
import cv2
import numpy as np


#stream = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=(fraction)120/1, format=(string)NV12 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink", cv2.CAP_GSTREAMER)

stream = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !appsink")

#code taken from:
#https://www.codemade.io/fast-and-accurate-face-tracking-in-live-video-with-python/

detector = dlib.get_frontal_face_detector()

def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2
 
    # Top left drawing
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
 
    # Top right drawing
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
 
    # Bottom left drawing
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
 
    # Bottom right drawing
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

def draw_axis(img, width, height, thickness, color):
    cv2.line(img, (width // 2, height - 1), (width // 2, 0), color, thickness)
    cv2.line(img, (0, height // 2), (width - 1, height // 2), color, thickness) 
 
bg_w = 500#px
bg_h = 500#px
background = np.zeros((bg_h, bg_w, 3), np.uint8)

margin = 50

key = 0

while key != 27:
    # read frames from live web cam stream
    (grabbed, frame) = stream.read()
 
    # resize the frames to be smaller and switch to gray scale
    #frame = imutils.resize(frame, width=700)
    
    #rotate image 90 degrees
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    # detect faces in the gray scale frame
    #face_rects = detector(gray, 0)
    face_rects = detector(rgb, 1)    
    face = None
 
    backdrop = background.copy()

    # loop over the face detections
    for i, d in enumerate(face_rects):
        x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()

        dx = x2 - x1
        dy = y2 - y1

        #print(str.format('[%04d x %04d]' % (dx, dy)))                

        #face = frame[y1:y2, x1:x2]        
        face = frame[y1-margin:y2+margin, x1-margin:x2+margin]

        face_w = dx + 2 * margin
        face_h = dy + 2 * margin

        #draw_axis(face, face_w, face_h, 2, (255, 0, 0))

        x_off = (bg_w - face_w) // 2
        y_off = (bg_h - face_h) // 2

        try:

            backdrop[y_off:y_off+face_h, x_off:x_off+face_w] = face          
        except:
            print("face is too big")

    cv2.imshow('face', face)

    key = cv2.waitKey(10)   
    
    # draw a fancy border around the faces
    #draw_border(overlay, (x1, y1), (x2, y2), (162, 255, 0), 2, 10, 10)
 
    # make semi-transparent bounding box
    #cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
 
 
# cleanup
cv2.destroyAllWindows()
stream.release()
