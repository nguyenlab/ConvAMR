#!/bin/bash


echo "Install pytorch for python 3.6 using miniconda 3"
conda install pytorch torchvision -c pytorch

# Install python dependencies

echo "Activate python 3.6 environments"
source activate py36

pip install nltk==3.2.5
pip install cffi
pip install numpy
pip install tqdm



# Clone SMATCH score

git clone https://github.com/snowblink14/smatch.git

git clone https://github.com/mdtux89/amr-evaluation.git
