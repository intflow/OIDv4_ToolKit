import os
import cv2
import numpy as np
from tqdm import tqdm
import argparse
import fileinput

# function that turns XMin, YMin, XMax, YMax coordinates to normalized yolo format
def convert(filename_str, coords):
	os.chdir("..")
	image = cv2.imread(filename_str + ".jpg")
	coords[2] -= coords[0]
	coords[3] -= coords[1]
	x_diff = int(coords[2]/2)
	y_diff = int(coords[3]/2)
	coords[0] = coords[0]+x_diff
	coords[1] = coords[1]+y_diff
	coords[0] /= int(image.shape[1])
	coords[1] /= int(image.shape[0])
	coords[2] /= int(image.shape[1])
	coords[3] /= int(image.shape[0])
	os.chdir("Label")
	return coords

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', help='input data path where label and meta folders are located',
						default='Y:/OID')
	parser.add_argument('--class_list', type=str, help='set label of classes in dataset',
						default='classes.txt')
	args = parser.parse_args()
	
	HOME = args.data_path
	CLASS_LIST = args.class_list
	

	# create dict to map class names to numbers for yolo
	classes = {}
	with open(CLASS_LIST, "r") as myFile:
		for num, line in enumerate(myFile, 0):
			line = line.rstrip("\n")
			classes[line] = num
		myFile.close()

	# step into dataset directory
	os.chdir(HOME)
	DIRS = os.listdir(os.getcwd())

	# for all train, validation and test folders
	for DIR in DIRS:
		if os.path.isdir(DIR):
			os.chdir(DIR)
			print("Currently in subdirectory:", DIR)
			
			CLASS_DIRS = os.listdir(os.getcwd())
			# for all class folders step into directory to change annotations
			for CLASS_DIR in CLASS_DIRS:
				if os.path.isdir(CLASS_DIR):
					os.chdir(CLASS_DIR)
					print("Converting annotations for class: ", CLASS_DIR)
					
					# Step into Label folder where annotations are generated
					os.chdir("Label")

					for filename in tqdm(os.listdir(os.getcwd())):
						filename_str = str.split(filename, ".")[0]
						if filename.endswith(".txt"):
							annotations = []
							with open(filename) as f:
								for line in f:
									labels = line.split()	

									#Change space to '_' in class name
									if type(line[1]) is str:
										labels[0] = labels[0]+'_'+labels[1]
										labels[1:] = labels[2:]

									for class_type in classes:
										if class_type == labels[0]:
											labels[0] = classes[class_type]
											coords = np.asarray([float(labels[1]), float(labels[2]), float(labels[3]), float(labels[4])])
											coords = convert(filename_str, coords)
											labels[1], labels[2], labels[3], labels[4] = coords[0], coords[1], coords[2], coords[3]
											newline = str(labels[0]) + " " + str(labels[1]) + " " + str(labels[2]) + " " + str(labels[3]) + " " + str(labels[4])
											annotations.append(newline)
								f.close()
							os.chdir("..")
							with open(filename, "w") as outfile:
								for line in annotations:
									outfile.write(line)
									outfile.write("\n")
								outfile.close()
							os.chdir("Label")
					os.chdir("..")
					os.chdir("..")
			os.chdir("..")

if __name__ == '__main__':
	main()