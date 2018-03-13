#!/bin/bash

PROJECT_ROOT=`pwd`

DATASET=LDC2017T10
CORPUS=$PROJECT_ROOT/corpus/$DATASET
DATA_BIN=$PROJECT_ROOT/data-bin/$DATASET

# clean tmp

mkdir -p $PROJECT_ROOT/tmp
rm -rf $PROJECT_ROOT/tmp/*


# create data-bin directory
mkdir -p $DATA_BIN

# merge files
cat $CORPUS/training/* > $PROJECT_ROOT/tmp/train.LDC2017T12.amr.txt
cat $CORPUS/dev/* > $PROJECT_ROOT/tmp/valid.LDC2017T12.amr.txt
cat $CORPUS/test/* > $PROJECT_ROOT/tmp/test.LDC2017T12.amr.txt

# linearize AMR graph
# create Named Entity, Part-of-speech
python -m amr.preprocess --linearize \
                         --input $PROJECT_ROOT/tmp/train.LDC2017T12.amr.txt \
                         --out_dir $DATA_BIN \
                         --prefix train

python -m amr.preprocess --linearize \
                         --input $PROJECT_ROOT/tmp/valid.LDC2017T12.amr.txt \
                         --out_dir $DATA_BIN \
                         --prefix valid


python -m amr.preprocess --linearize \
                         --input $PROJECT_ROOT/tmp/test.LDC2017T12.amr.txt \
                         --out_dir $DATA_BIN \
                         --prefix test

# Create indexed data by Fairseq
python preprocess.py --source-lang snt \
                     --target-lang amr \
                     --trainpref $DATA_BIN/train \
                     --validpref $DATA_BIN/valid \
                     --testpref $DATA_BIN/test \
                     --destdir $DATA_BIN
