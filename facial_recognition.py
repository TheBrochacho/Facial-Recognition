import process_faces 

import threading
import time
import os
import cv2
import _pickle
import imutils
import face_recognition
import pyttsx3
import queue
import random

#https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

class file_watchdog(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		
		self.unsorted = "unsorted"
		
		print('[INFO] starting folder watchdog')
		
	def run(self):
		while True:
			if len(os.listdir(self.unsorted)) > 0:
				break
			
			print('[INFO] No new files.')
			time.sleep(10)
			
class big_brother(threading.Thread):
	def __init__(self, threadID, name, counter, q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.q = q
		
		print('[INFO] starting Big Brother')
		
	def run(self):
		fp = process_faces.face_processor()

		print('[INFO] starting camera')
		
		cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink", cv2.CAP_GSTREAMER)		
	
		encodings_file="pickle.encodings"
		detection = "cnn"
		margin = 440
	
		while True:
			fw_thread = file_watchdog(2, 'watchdog', 2)
			fw_thread.start()
	
			print("[INFO] loading encodings...")
			data = _pickle.loads(open(encodings_file, "rb").read())
			print("[INFO] faces in database", len(data["encodings"]))

			while fw_thread.isAlive():
				try:
					re, img = cap.read()
	
					img = imutils.resize(img, width=400)
					img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)	
	
					rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

					# detect the (x, y)-coordinates of the bounding boxes corresponding
					# to each face in the input image, then compute the facial embeddings
					# for each face
					#print("[INFO] recognizing faces...")
	
					boxes = face_recognition.face_locations(rgb, model=detection)
					faces = face_recognition.face_encodings(rgb, boxes)
	
					if len(faces) > 0:
						# initialize the list of names for each face detected
						#names = []
	
						# loop over the facial embeddings
						for face in faces:
							# attempt to match each face in the input image to our known
							# encodings
		
							#lower tolerance => more strict (default is 0.6)
							matches = face_recognition.compare_faces(data["encodings"], face, tolerance=0.5)
							name = "Unknown"
						
							counts = {}
		
							for (i, match) in enumerate(matches):

								# find the indexes of all matched faces then initialize a
								# dictionary to count the total number of times each face
								# was matched
								if match:
									name = data["names"][i]
									counts[name] = counts.get(name, 0) + 1
		
							# determine the recognized face with the largest number of
							# votes (note: in the event of an unlikely tie Python will
							# select first entry in the dictionary)
							if len(counts) > 0:
								name = max(counts, key=counts.get)
								print(name)
								self.store_face_in_queue(name)

				except KeyboardInterrupt:
					print("[INFO] manually terminated program")
					cap.release()
					try:					
						fw_thread.join()
					except:
						print("¯\_(ツ)_/¯")
					break
			fp.process_faces()
			fp.encode_faces()

	def store_face_in_queue(self, name='Unknown'):
		if name != 'Unknown':
			lock.acquire()
			names = self.q.get()
			names[name] = names.get(name, 0) + 1
			self.q.put(names)
			lock.release()
	
class tts_greeter(threading.Thread):
	def __init__(self, threadID, name, counter, q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		
		self.q = q
		
		self.mouth = pyttsx3.init()
		self.mouth.setProperty('rate', 150)
		self.mouth.setProperty('volume', 1.0)
		self.mouth.setProperty('voice', 'english-us')
				
		self.mouth.connect('finished-utterance', self._clear_queue)
		
		self._templates = []
		with open('greetings.txt', 'r') as f:
			self._templates = f.readlines()
			
		self._last_greeted = None
		
		print('[INFO] starting text-to-speech bot')
	
	
	def message(self):	
		ret_val = None
		
		lock.acquire()
		names = self.q.get()
		
		if len(names) > 0:
			name=max(names, key=names.get)
			if name != self._last_greeted:
				ret_val = random.choice(self._templates).format(name=name.split()[0])
				self._last_greeted = name

		self.q.put({})
		lock.release()
			
		return ret_val
		
	def run(self):
		while True:
			greeting = self.message()
		
			if greeting != None:
				self.mouth.say(greeting, self._last_greeted)
				print(greeting)
				self.mouth.runAndWait()
		
	def _clear_queue(self, name, completed):
		#print("finished", name)
		self.q.get()
		self.q.put({})
		
		
if __name__ == '__main__':

	global lock
	lock = threading.Lock()
	
	q = queue.Queue(maxsize=1)
	q.put({})
	
	big_bro = big_brother(1, "Big Brother", 1, q)
	tts_bot = tts_greeter(3, "Salutations", 3, q)
	
	big_bro.start()
	tts_bot.start()
	
