#!/bin/bash

python3 main.py downloader --classes Monkey \
                          --type_csv train \
                          --Dataset /DL_data/OID \
                          --yes \
                          --limit 500 \
                          --multiclasses 0 \
                          --image_IsGroupOf 0 \
                          --n_threads 32

#python3 main.py downloader --classes Person Motorcycle \
#                          --type_csv validation \
#                          --Dataset /DL_data/OID \
#                          --yes \
#                          --limit 500 \
#                          --multiclasses 1 \
#                          --image_IsGroupOf 0 \
#                          --n_threads 32

#python3 main.py downloader --classes Person Motorcycle \
#                          --type_csv test \
#                          --Dataset /DL_data/OID \
#                          --yes \
#                          --limit 500 \
#                          --multiclasses 1 \
#                          --image_IsGroupOf 0 \
#                          --n_threads 32


