import os
import cv2
import numpy as np
from tqdm import tqdm
import argparse
import fileinput
import shutil

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
						default='Y:/OID_jetson_test')
	parser.add_argument('--class_list', type=str, help='set label of classes in dataset',
						default='classes.txt')
	parser.add_argument('--tag', type=str, help='set label of classes in dataset',
						default='Monkey50')
	parser.add_argument('--img_x', type=int, help='set x resolution',
						default=640)
	parser.add_argument('--img_y', type=int, help='set y resolution',
						default=480)
	args = parser.parse_args()
	
	HOME = args.data_path
	CLASS_LIST = args.class_list
	TAG = args.tag
	TARGET_X = args.img_x
	TARGET_Y = args.img_y
	

	# create dict to map class names to numbers for yolo
	#classes = {}
	#with open(CLASS_LIST, "r") as myFile:
	#	for num, line in enumerate(myFile, 0):
	#		line = line.rstrip("\n")
	#		classes[line] = num
	#	myFile.close()

	# step into dataset directory
	os.chdir(HOME)
	DIRS = os.listdir(os.getcwd())
	KITTI_PATH = HOME+'_kitti'+'/'+TAG
	KITTI_IMAGE_PATH = KITTI_PATH+'/image_2'
	KITTI_LABEL_PATH = KITTI_PATH+'/label_2'

	# Make kitti folder structure
	if not os.path.exists(KITTI_PATH):
		os.makedirs(KITTI_PATH)
	if not os.path.exists(KITTI_IMAGE_PATH):
		os.makedirs(KITTI_IMAGE_PATH)
	if not os.path.exists(KITTI_LABEL_PATH):
		os.makedirs(KITTI_LABEL_PATH)

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

						# Copy every files to kitti folders
						FULL_PATH = HOME + '/' + DIR + '/' + CLASS_DIR

						#Resize image
						img_src = cv2.imread(FULL_PATH+'/'+filename_str+'.jpg', cv2.IMREAD_COLOR)
						size_src = img_src.shape
						ratio_src = size_src[1] / size_src[0]
						ratio_target = TARGET_X / TARGET_Y
						
						border_x = 0
						if ratio_src < ratio_target:
							target_x = size_src[0] * ratio_target
							border_x = int((target_x - size_src[1]) * 0.5)
							img_src = cv2.copyMakeBorder(img_src, 0, 0, border_x, border_x, cv2.BORDER_CONSTANT)
							size_src = img_src.shape
							
						dst = cv2.resize(img_src, dsize=(TARGET_X, TARGET_Y), interpolation=cv2.INTER_AREA)
						cv2.imwrite(KITTI_IMAGE_PATH+'/'+filename_str+'.jpg', dst)
						r_x = TARGET_X / size_src[1]
						r_y = TARGET_Y / size_src[0]
						
						#Revise Label
						annotations = []
						f_o = open(KITTI_LABEL_PATH+'/'+filename_str+'.txt', 'w')
						with open(FULL_PATH+'/Label/'+filename_str+'.txt') as f:
							for line in f:
								labels = line.split()

								pos_x1 = float(labels[1])
								pos_y1 = float(labels[2])
								pos_x2 = float(labels[3])
								pos_y2 = float(labels[4])

								if ratio_src < ratio_target:
									pos_x1 = int((border_x + pos_x1) * r_x)
									pos_x2 = int((border_x + pos_x2) * r_x)
								else:
									pos_x1 = int(pos_x1 * r_x)
									pos_x2 = int(pos_x2 * r_x)
								
								pos_y1 = int(pos_y1 * r_y)
								pos_y2 = int(pos_y2 * r_y)

								line_modif = labels[0].lower() + ' 0.0 0 0.0 ' + str(pos_x1) + ' ' +str(pos_y1) + ' ' + str(pos_x2) + ' ' +str(pos_y2) + ' 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n'
								

								f_o.write(line_modif)
								##Change space to '_' in class name
								#try:
								#	float(labels[1])
								#except:
								#	labels[0] = labels[0]+' '+labels[1]
								#	labels[1:] = labels[2:]
								#for class_type in classes:
								#	if labels[0] in str.split(class_type, "_"):
								#		labels[0] = classes[class_type]
								#		coords = np.asarray([float(labels[1]), float(labels[2]), float(labels[3]), float(labels[4])])
								#		coords = convert(filename_str, coords)
								#		labels[1], labels[2], labels[3], labels[4] = coords[0], coords[1], coords[2], coords[3]
								#		newline = str(labels[0]) + " " + str(labels[1]) + " " + str(labels[2]) + " " + str(labels[3]) + " " + str(labels[4])
								#		annotations.append(newline)
							f.close()
							f_o.close()

if __name__ == '__main__':
	main()