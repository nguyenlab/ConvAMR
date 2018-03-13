import argparse
import io
import subprocess
import itertools

from os.path import join
from amr.utils import read_amr_format, save_amr_format
from amr.linearize import delinearize
from multiprocessing import Pool


def read_fairseq_output_fairseq(path):
  with io.open(path, encoding='utf-8') as f:
    lines = f.readlines()
  n_line = len(lines)
  data = []
  for i in range(0, n_line, 4):
    sent_parts = lines[i].strip().split('\t')
    id = sent_parts[0][2:]
    snt = sent_parts[1]
    prefix_l = len(sent_parts[0]) + 1
    linear_amr = lines[i + 1].strip()[prefix_l:]
    amr_lines = delinearize(linear_amr)
    sample = {'id': id,
              'snt': snt,
              'linear_amr': linear_amr,
              'doc': amr_lines}
    data.append(sample)
  data = sorted(data, key=lambda a: int(a['id']))
  return data


def read_fairseq_output_neuralamr(path):
  with io.open(path, encoding='utf8') as f:
    lines = f.readlines()
  n_line = len(lines)
  data = {}
  for i in range(0, n_line, 4):
    sent_parts = lines[i].strip().split('\t')
    id = sent_parts[0][2:]
    snt = sent_parts[1]
    prefix_l = len(sent_parts[0]) + 1
    linear_amr = lines[i + 1].strip()[prefix_l:]
    sample = {'id': id,
              'snt': snt,
              'linear_amr': linear_amr}
    data[id] = sample
  data = sorted(data.values(), key=lambda a: int(a['id']))
  print('Number of samples: %d' % (len(data)))
  return data


def deAnonymize_neural_amr(deanonymizer_path, stripped_text):
  command = [deanonymizer_path,
             'deAnonymizeAmr',
             'false',
             stripped_text]
  process = subprocess.Popen(command, stdout=subprocess.PIPE)
  out, error = process.communicate()
  if out.startswith('('):
    amr = str(out).split('#')[0]
    #print('| AMR: ' + amr)
    return amr
  else:
    print('None output')
    return "(a / a)"


def deAnonymize_wrapper(arg):
  return deAnonymize_neural_amr(*arg)

def evaluate(sys_path, gold_path):
  import subprocess
  command = 'python -m smatch.smatch -f %s %s' % (sys_path, gold_path)
  subprocess.call(command.split(' '))


# Define params
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-s', '--system', required=True, help='Output of the fairseq system')
# params for model choosing
parser.add_argument('--fairseq', default=False, action='store_true',
                    help='Post process for Fairseq format')
parser.add_argument('--neuralamr', default=False, action='store_true',
                    help='Post process for NeuralAMR format')

# params for neural AMR
parser.add_argument('--sentenceFile', default='',
                    help='The sentence file that contains list of sentence')
parser.add_argument('--deAnon', default='', help='Path to anonDeAnon_java.sh')

# parser.add_argument('-g', '--gold', required=True, help='Gold test data')
args = parser.parse_args()

if args.fairseq:
  # Define file path
  system_fairseq_path = args.system
  system_amr_path = join('tmp', system_fairseq_path.replace('/', '_'))
  # gold_path = args.gold

  # Read data
  amr_data = read_fairseq_output_fairseq(system_fairseq_path)
  # gold_data = read_amr_format(args.gold)
  # Post process
  print('Save AMR file..')
  save_amr_format(amr_data, system_amr_path, end='\n')
  # evaluate(system_amr_path, gold_path)
elif args.neuralamr:
  if args.sentenceFile:
    print('System output: %s'%(args.system))
    print('Sentence output: %s'%(args.sentenceFile))

    # Define file path
    system_fairseq_path = args.system
    system_tmp_path = join('tmp', system_fairseq_path.replace('/', '_') + '.tmp')
    # Read the source sentence
    with io.open(args.sentenceFile, 'r', encoding='utf8') as f:
      sentences = f.readlines()
    # Read stripped data
    stripped_data = read_fairseq_output_neuralamr(system_fairseq_path)
    text_lines = []
    # Check whether this two files has the same number of instances
    if len(sentences) == len(stripped_data):
      stripped_data = [x['linear_amr'] for x in stripped_data]

      pool = Pool(20)
      n_sample = len(stripped_data)
      result = pool.map(deAnonymize_wrapper,
                        zip([args.deAnon]*n_sample, stripped_data))
      for idx, (snt, amr_text) in enumerate(zip(sentences, result)):
        text_lines.append('\n# ::id  %d' % (idx))
        text_lines.append('# ::snt  %s' % (snt.strip()))
        text_lines.append(amr_text)

      system_output_path = system_tmp_path + '.amr.txt'
      print('Save file at: ' + system_output_path)
      with io.open(system_output_path, 'w', encoding='utf8') as f:
        f.write('\n'.join(text_lines))
    else:
      print('Two files are different in number of sentences. Exit')
  else:
    print('Please provide the --sentenceFile option')
