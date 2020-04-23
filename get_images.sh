#!/bin/bash

python3 main.py downloader --classes Human_body \
                          --type_csv all \
                          --Dataset /DL_data/OID \
                          --limit 30 \
                          --image_IsOccluded 0 \
                          --image_IsTruncated 0 \
                          --image_IsGroupOf 0 \
                          --image_IsDepiction 1 \
                          --image_IsInside 0 \
                          --multiclasses 0 \
                          --n_threads 32

