from amr.linearize import linearize
from os.path import join, basename
from multiprocessing import Pool
from nltk.tokenize import TweetTokenizer
from amr.utils import read_amr_format
import codecs
import argparse
import os

tokenizer = TweetTokenizer()


def save(sentences, file_path):
    text = '\n'.join(sentences)
    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)


def split(data):
    '''
    data: a list of object
    '''
    train, valid, test = [], [], []
    for idx, sample in enumerate(data):
        if idx % 5 == 0:
            test.append(sample)
        elif idx % 5 == 1:
            valid.append(sample)
        else:
            train.append(sample)
    return train, valid, test


def preprocess_feature(obj):
    # preprocess sentence
    tokens = tokenizer.tokenize(obj['snt'])
    snt = ' '.join(tokens)
    # preprocess amr
    linear_amr = linearize(obj['doc'])
    return (snt, linear_amr, obj)


############ TEST ####################

parser = argparse.ArgumentParser()
parser.add_argument('--linearize', default=False,
                    action='store_true', help='Linearize the given file')
parser.add_argument('--delinearize', default=False,
                    action='store_true', help='De-linearize the given file')

parser.add_argument('--input', required=True, help='Input file path')
parser.add_argument('--out_dir', required=True, help='Output directory')
parser.add_argument('--prefix', required=True, help='Output file prefix')

args = parser.parse_args()

if args.linearize:
    p = Pool(20)
    print('Linearize file: %s' % (args.input))
    data = read_amr_format(args.input
                           , return_dict=False)
    sentences = [x['snt'] for x in data]
    amrs = [x['doc'] for x in data]
    amrs_linearized = p.map(linearize, amrs)
    save(sentences, join(args.out_dir, '%s.snt' % (args.prefix)))
    save(amrs_linearized, join(args.out_dir, '%s.amr' % (args.prefix)))

elif args.delinearize:
    pass
