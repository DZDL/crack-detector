#!/bin/bash

# GPU_IDS=$1

DATAROOT=./datasets/DeepCrack
NAME=deepcrack
MODEL=deepcrack
DATASET_MODE=deepcrack

BATCH_SIZE=1
NORM=batch

NUM_CLASSES=1
NUM_TEST=10000

python3 DeepSegmentor/test.py \
  --dataroot ${DATAROOT} \
  --name ${NAME} \
  --model ${MODEL} \
  --dataset_mode ${DATASET_MODE} \ 
  --batch_size ${BATCH_SIZE} \
  --num_classes ${NUM_CLASSES} \
  --norm ${NORM} \
  --num_test ${NUM_TEST}\
  --display_sides 1


#  --gpu_ids ${GPU_IDS} \  