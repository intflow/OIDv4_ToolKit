#!/bin/bash

python3 main.py downloader --classes Motorcycle Bicycle \
                          --type_csv train \
                          --Dataset /DL_data/OID \
                          --yes \
                          --limit 5000 \
                          --multiclasses 1 \
                          --n_threads 32

python3 main.py downloader --classes Motorcycle Bicycle \
                          --type_csv validation \
                          --Dataset /DL_data/OID \
                          --yes \
                          --limit 200 \
                          --multiclasses 1 \
                          --n_threads 32

python3 main.py downloader --classes Motorcycle Bicycle \
                          --type_csv test \
                          --Dataset /DL_data/OID \
                          --yes \
                          --limit 100 \
                          --multiclasses 1 \
                          --n_threads 32


