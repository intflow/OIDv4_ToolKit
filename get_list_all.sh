#!/bin/bash

python get_list.py --data_path "/DL_data/OID/train/Human body" --list_file "train1.txt"
python get_list.py --data_path "/DL_data/OID/test/Human body" --list_file "test1.txt"
python get_list.py --data_path "/DL_data/OID/train/Motorcycle_Bicycle" --list_file "train2.txt"
python get_list.py --data_path "/DL_data/OID/test/Motorcycle_Bicycle" --list_file "test2.txt"
