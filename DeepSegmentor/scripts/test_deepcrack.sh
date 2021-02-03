#!/bin/bash

# GPU_IDS=$1

# DATAROOT=./datasets/DeepCrack
# NAME=deepcrack
# MODEL=deepcrack
# DATASET_MODE=deepcrack

# BATCH_SIZE=1
# NORM=batch

# NUM_CLASSES=1
# NUM_TEST=10000

python3 DeepSegmentor/test.py \
  --dataroot ./DeepSegmentor/datasets/DeepCrack \
  --name deepcrack \
  --model deepcrack \
  --dataset_mode deepcrack \ 
  --batch_size 1 \
  --num_classes 1 \
  --norm batch \
  --num_test 10000 \
  --display_sides 1

# python3 DeepSegmentor/test.py \
#   --dataroot ${DATAROOT} \
#   --name ${NAME} \
#   --model ${MODEL} \
#   --dataset_mode ${DATASET_MODE} \ 
#   --batch_size ${BATCH_SIZE} \
#   --num_classes ${NUM_CLASSES} \
#   --norm ${NORM} \
#   --num_test ${NUM_TEST}\
#   --display_sides 1


#  --gpu_ids ${GPU_IDS} \  