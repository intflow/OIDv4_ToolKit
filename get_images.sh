#!/bin/bash

python3 main.py downloader --classes Human_body \
                          --type_csv all \
                          --Dataset /DL_data/OID2 \
                          --yes \
                          --limit 5000 \
                          --multiclasses 0 \
                          --n_threads 32

