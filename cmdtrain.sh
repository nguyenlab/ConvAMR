#!/bin/bash



source activate py36

MODEL_DIR=models/LDC2017T10
mkdir -p $MODEL_DIR

export CUDA_VISIBLE_DEVICES=0

python train.py data-bin/LDC2017T10 \
  --lr 0.25 \
  --clip-norm 0.1 \
  --dropout 0.2 \
  --max-tokens 4000 \
  --arch fconv_iwslt_de_en \
  --save-dir $MODEL_DIR

