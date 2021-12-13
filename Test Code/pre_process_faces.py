import os

def move_to_folders(unsorted_path="Unsorted", sorted_path="Faces"):
	for (root, dirs, files) in os.walk(unsorted_path):
		for image in files:
			file_index = 0
		
			if ".JPG" in image:
				folder = ''.join([i for i in image if not i.isdigit()]).replace('.JPG', '').strip()
				
				print(folder)
			
				local = os.path.join(sorted_path, folder)
				if not os.path.exists(local):
					os.mkdir(local)
					
				while True:
					filename = str.format("%d.JPG" % (file_index))
					new_path = os.path.join(sorted_path, folder, filename)
					
					file_index += 1
					
					if not os.path.exists(new_path):
						file_index = 0
						break
				
				old_path = os.path.join(root, image)
				
				os.rename(old_path, new_path)

