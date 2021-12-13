How to run the facial recognition:
run facial_recognition.py from this directory


If you want to add more images to the dataset:
1. Make sure the image is a .jpg file
2. Make sure the image file name follows this format:
	
	John Smith XXX.jpg
	
   (where XXX is a placeholder for a number)
3. Move the file(s) into the "unsorted" folder within this directory.
   The program will see them, add them to the dataset, retrain itself, and
   restart the facial recognition.


To add more greetings:

1. Open "greetings.txt"
2. on a new line simply type another greeting
	- The greeting needs to follow the format of:

	ex:	Hello {name}
	
	- {name} will get substituted with an actual name at runtime.
	- because it's read via Text to Speech, the spelling may have
	  to be tweaked to get the desired pronunciation