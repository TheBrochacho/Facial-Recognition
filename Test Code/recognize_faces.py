#referenced code from:
#https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

import face_recognition
import _pickle
import cv2
import imutils

def recognize_faces(encodings_file="pickle.encodings"):

	detection = "CNN"

	margin = 440

	print("[INFO] loading encodings...")
	data = _pickle.loads(open(encodings_file, "rb").read())
	print("[INFO] faces in database", len(data["encodings"]))

	#cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink", cv2.CAP_GSTREAMER)

	cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=(fraction)120/1, format=(string)NV12 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink", cv2.CAP_GSTREAMER)

	while True:
		re, img = cap.read()
	
		img = imutils.resize(img, width=400)
		img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)	
	
		#rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		
		rgb = img[:, :, ::-1]		

		# detect the (x, y)-coordinates of the bounding boxes corresponding
		# to each face in the input image, then compute the facial embeddings
		# for each face
		#print("[INFO] recognizing faces...")
	
		boxes = face_recognition.face_locations(rgb, model=detection)
		faces = face_recognition.face_encodings(rgb, boxes)
	
		if len(faces) > 0:
			# initialize the list of names for each face detected
			names = []
	
			# loop over the facial embeddings
			for face in faces:
				# attempt to match each face in the input image to our known
				# encodings
		
				matches = face_recognition.compare_faces(data["encodings"], face)
				name = "Unknown"
		
				for (i, match) in enumerate(matches):
					
					# find the indexes of all matched faces then initialize a
					# dictionary to count the total number of times each face
					# was matched
					counts = {}
		
					if match:
						name = data["names"][i]
						print(name)
						counts[name] = counts.get(name, 0) + 1
			
					# determine the recognized face with the largest number of
					# votes (note: in the event of an unlikely tie Python will
					# select first entry in the dictionary)
					if len(counts) > 0:
						name = max(counts, key=counts.get)
	
				# update the list of names
				names.append(name)
	
			# loop over the recognized faces
			for ((top, right, bottom, left), name) in zip(boxes, names):
				# draw the predicted face name on the image
				cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
				y = top - 15 if top - 15 > 15 else top + 15
				cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
					0.75, (0, 255, 0), 2)
		 
		# show the output image
		cv2.imshow("Image", img)
	
		key = cv2.waitKey(10)
		if key == 27:
			break
			
if '__main__':
	recognize_faces()
