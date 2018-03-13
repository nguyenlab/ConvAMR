from amr.linearize import linearize, delinearize
from utils import read_amr_format, save_amr_format
from os import listdir
from os.path import join

import subprocess


GOLD_AMR = 'corpus/'

for fname in listdir(GOLD_AMR):

  # data = read_amr_format(join(GOLD_AMR, fname))
  # result = []
  #
  print(fname)

  OUTPUT_AMR = 'tmp/delinearied.%s'%(fname)
  # for sample in data:
  #   lines = sample['doc']
  #   linearized_text = linearize(lines)
  #   delinearize_text = delinearize(linearized_text)
  #   sample['doc'] = delinearize_text
  #   result.append(sample)
  command = 'python -m amr.smatch.smatch -f %s %s' % (join(GOLD_AMR, fname)
                                                      , OUTPUT_AMR)


  # save_amr_format(result, OUTPUT_AMR)
  subprocess.call(command.split(' '))