import os
import argparse




def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', help='input data path where label and meta folders are located',
						default='Y:/OID/train/Human body')
	parser.add_argument('--list_file', help='list file name',
						default='train_1.txt')
	args = parser.parse_args()
	HOME = args.data_path
	FNAME = args.list_file

	f = open(FNAME, 'w')
	for root, dirs, files in os.walk(os.path.abspath(HOME)):
		for file in files:
			if file.split('.')[-1] == 'jpg':
				print(os.path.join(root, file))
				f.write(str(os.path.join(root, file))+'\n')
	f.close
if __name__ == '__main__':
	main()