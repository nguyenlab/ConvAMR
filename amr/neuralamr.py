from amr.linearize import linearize
from os.path import join
from multiprocessing import Pool
from nltk.tokenize import TweetTokenizer
from amr.utils import read_amr_format
from amr.utils import save_amr_format
import codecs

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


def preprocess(obj):
  # preprocess sentence
  tokens = tokenizer.tokenize(obj['snt'])
  snt = ' '.join(tokens)
  # preprocess amr
  linear_amr = linearize(obj['doc'])
  return (snt, linear_amr, obj)


############ TEST ####################

if __name__ == '__main__':
  CORPUS = 'corpus/'
  OUTPUT = 'data/LDC2014.snt-amr/'
  OUTPUT = 'data/civilcode.snt-amr/'
  data_file = ['amr-release-1.0-bolt.txt',
               'amr-release-1.0-consensus.txt',
               'amr-release-1.0-dfa.txt',
               'amr-release-1.0-mt09sdl.txt',
               'amr-release-1.0-proxy.txt',
               'amr-release-1.0-xinhua.txt',
               ]
  data_file = ['civilcode-1.0.txt']
  data = []
  for fname in data_file:
    data += read_amr_format(join(CORPUS, fname))

  p = Pool(20)
  result = p.map(preprocess, data)
  # train, valid, test = split(result)
  # save([u for u, l, a in train], join(OUTPUT, 'train.snt'))
  # save([l for u, l, a in train], join(OUTPUT, 'train.amr'))
  # save([u for u, l, a in valid], join(OUTPUT, 'valid.snt'))
  # save([l for u, l, a in valid], join(OUTPUT, 'valid.amr'))
  # save([u for u, l, a in test], join(OUTPUT, 'test.snt'))
  # save([l for u, l, a in test], join(OUTPUT, 'test.amr'))

  save([u for u, l, a in result], join(OUTPUT, 'amr-test.snt'))
  save([l for u, l, a in result], join(OUTPUT, 'amr-test.amr'))

  #save_amr_format([a for u, l, a in test], join(OUTPUT, 'test.amr.txt'),end='')
