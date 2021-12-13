import os
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import numpy as np

#code referenced from:
#https://www.codemade.io/fast-and-accurate-face-tracking-in-live-video-with-python/
#https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
fa = FaceAligner(predictor, desiredFaceWidth=288)

"""
bg_w = 400#px
bg_h = 400#px
background = np.zeros((bg_h, bg_w, 3), np.uint8)
"""


bad_img_cnt = 0
bad_img_path = "../bad"

for (root, dirs, files) in os.walk('Faces'):
	
	"""
	bad_img_path = os.path.join(root, bad_img_path)
	print(bad_img_path)
	"""
	
	for folder in dirs:
		local = os.path.join(root, folder)
		images = os.listdir(local)
		
		print(folder)
		
		for img in images:
			if '.JPG' in img:
			
				new = local.replace("Faces", "dataset")
				if not os.path.exists(new):
					os.mkdir(new)
					print("created folder", new)
				
				new = os.path.join(new, img)
				if not os.path.exists(new):
							                
					frame = cv2.imread(os.path.join(local, img))

					frame = imutils.resize(frame, width=800)

					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

					# detect faces in the gray scale frame
					face_rects = detector(gray, 1)

					for i, d in enumerate(face_rects):
				
						"""
						shape = predictor(gray, d)
						shape = face_utils.shape_to_np(shape)
					
						for (x, y) in shape:
							cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
						"""	
						(x, y, w, h) = rect_to_bb(d)
						faceAligned = fa.align(frame, gray, d)
						#cv2.imshow("aligned", faceAligned)
					
					cv2.imwrite(new, faceAligned)
					print("saved image to:", new)	
					
					
					"""
					x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
									
					try:               
						dx = x2 - x1
						dy = y2 - y1
						faces.append((dx, dy))

						print(str.format('[%04d x %04d]' % (dx, dy)))                

						face = frame[y1-margin:y2+margin, x1-margin:x2+margin].copy()

						face_w = dx + 2 * margin
						face_h = dy + 2 * margin

						draw_axis(face, face_w, face_h, 2, (255, 0, 0))

						x_off = (bg_w - face_w) // 2
						y_off = (bg_h - face_h) // 2

						backdrop[y_off:y_off+face_h, x_off:x_off+face_w] = face          
						
					except:
						print("face not found for", os.path.join(local, img))
				
				cv2.imshow('face', backdrop)
				"""
				"""
				if face_count == 0:
					print("face not found for", os.path.join(local, img))
					new = os.path.join(bad_img_path, str.format("%d%s" % (bad_img_cnt, img[1:])))
					print("moving", os.path.join(local, img)) 
					os.rename(os.path.join(local, img), new)
					
					bad_img_cnt += 1
				"""
				"""	
				key = 0
				while key != 27:
					key = cv2.waitKey(10)
				"""
# cleanup
cv2.destroyAllWindows()
