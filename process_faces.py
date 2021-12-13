import os
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
from imutils import paths
import numpy as np
import face_recognition
import _pickle

#code referenced from:
#https://www.codemade.io/fast-and-accurate-face-tracking-in-live-video-with-python/
#https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

#https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/


class face_processor:
	def __init__(self, dataset="dataset", unsorted="unsorted"):
		if not os.path.exists(dataset):
			os.mkdir(dataset)
			
		self.dataset = dataset
		self.unsorted = unsorted
			
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
		self.fa = FaceAligner(self.predictor, desiredFaceWidth=288)
		
	def process_faces(self):
		for (root, dirs, files) in os.walk(self.unsorted):
			for image in files:
			
				old_path = os.path.join(root, image)
			
				file_index = 0
		
				if '.JPG' or '.jpg' in image:
					image = image.replace('.jpg', '.JPG')
				
					folder = ''.join([i for i in image if not i.isdigit()]).replace('.JPG', '').strip()
			
					local = os.path.join(self.dataset, folder)
					
					print(local)
					
					if not os.path.exists(local):
						os.mkdir(local)
					
					while True:
						filename = str.format("%d.JPG" % (file_index))
						new_path = os.path.join(local, filename)
					
						file_index += 1
					
						if not os.path.exists(new_path):
							file_index = 0
							break
				
					self.process_face(old_path, new_path)
					
					os.remove(old_path)
					if len(os.listdir(local)) == 0:
						os.rmdir(local)
	
	def process_face(self, old_path, new_path):
		frame = cv2.imread(old_path)

		frame = imutils.resize(frame, width=800)

		rgb = frame[:, :, ::-1]
		#rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# detect faces in the gray scale frame
		face_rects = self.detector(rgb, 1)

		if (len(face_rects) > 0):
			for i, d in enumerate(face_rects):

				(x, y, w, h) = rect_to_bb(d)
				faceAligned = self.fa.align(frame, rgb, d)
				#cv2.imshow("aligned", faceAligned)
	
			cv2.imwrite(new_path, faceAligned)
			print("saved image to:", new_path)
		else:
			print("no face found in image:", old_path)
			
	
	def encode_faces(self):
		# grab the paths to the input images in our dataset
		print("[INFO] quantifying faces...")
		imagePaths = list(paths.list_images(self.dataset))
		 
		# initialize the list of known encodings and known names
		knownEncodings = []
		knownNames = []

		# loop over the image paths
		for (i, imagePath) in enumerate(imagePaths):
			# extract the person name from the image path
			name = imagePath.split(os.path.sep)[-2]

			print("[INFO] processing image {}/{}: {}".format(i + 1,
				len(imagePaths), imagePath))
	 
			# load the input image and convert it from BGR (OpenCV ordering)
			# to dlib ordering (RGB)
			image = cv2.imread(imagePath)
			
			"""
			cv2.imshow(name, image)
			key = 0
			while key != 27:
				key = cv2.waitKey(1)
			cv2.destroyAllWindows()
			"""			
			
			rgb = image[:, :, ::-1]
			#rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
			# detect the (x, y)-coordinates of the bounding boxes
			# corresponding to each face in the input image
			boxes = face_recognition.face_locations(rgb, model="cnn")
		 
			# compute the facial embedding for the face
			encodings = face_recognition.face_encodings(face_image=rgb, known_face_locations=boxes, num_jitters=100)
		 
			# loop over the encodings
			for encoding in encodings:

				# add each encoding + name to our set of known names and
				# encodings
				knownEncodings.append(encoding)
				knownNames.append(name)
		
		
		# dump the facial encodings + names to disk
		print("[INFO] serializing encodings...")
		data = {"encodings": knownEncodings, "names": knownNames}
		f = open("pickle.encodings", "wb")
		f.write(_pickle.dumps(data))
		f.close()
		print("[Info] finished encoding faces")
