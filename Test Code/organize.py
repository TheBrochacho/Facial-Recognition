import os

unsorted="Unsorted"
faces="Faces"

def move_to_folders(path):
	for (root, dirs, files) in os.walk(path):
		for file in files:
			folder = ""
			chars = [c for c in file if not str.isdigit(c)]
			for c in chars:
				folder += c
			folder.replace('.JPG', '')
			local = os.path.join(root, folder)
			if not os.path.exists(local):
				os.mkdir(local)
			old = os.path.join(root, file)
			new = os.path.join(local, file)
			os.rename(old, new)

def rename_files(path):
	for (root, dirs, files) in os.walk(path):
		for folder in dirs:
			local = os.path.join(root, folder)
			i = 0
			images = os.listdir(local)
			
			for image in images:
				old = os.path.join(local, images)
				name = str.format("%d.JPG" % (i))
				new = os.path.join(local, name)

				#print(old)
				print(new)								
				os.rename(old, new)
				i += 1


#for when you're a dipshit who runs rename_files twice and ends up doubling up on the folders
def unfuck():
	for (root, dirs, files) in os.walk('.'):
		for file in files:
			rename = False					
			
			path = os.path.join(root, file)
			paths = path.split('/')

			for p in paths:
				if paths.count(p) > 1:
					paths.remove(p)
					rename = True

			new = '/'.join(paths)
			
			if rename == True:
				os.rename(path, new)

	for (root, dirs, files) in os.walk('.'):
		for folder in dirs:
			local = os.path.join(root, folder)
			try:			
				if os.listdir(local) == []:
					os.rmdir(local)
			except:
				print(local)

#unfuck()
#move_to_folders("Unsorted")
rename_files("dataset")
