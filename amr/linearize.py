from __future__ import print_function
import argparse

DEBUG = False


class Node(object):
  def __init__(self, var, concept, is_constant=False):
    self.var = var
    self.concept = concept
    self.is_constant = is_constant


def linearize(lines):
  def normalize(line):
    return line.strip().replace('(', '( ').replace(')', ' )')

  # preprocess
  text = ''
  for line in lines:
    if len(text) > 0:
      text += ' ' + normalize(line)
    else:
      text = normalize(line)
  #sprint('Text: "%s"' % text)

  queue = []
  stack = []
  var_concept = {}
  prev = ""
  var = None

  for tok in text.split(' '):
    if len(tok) == 0:
      continue
    if DEBUG:
      print('--> "%s"' % (tok), end=',')
    if tok == '(':
      if DEBUG:
        print('Do nothing 1')
    elif tok == ')':
      node = stack.pop()
      queue.append(node.concept)
      if DEBUG:
        print('Pop stack')
        show(queue)
    elif tok == '/':
      if DEBUG:
        print('Do nothing 3')
    elif tok.startswith(':'):
      queue.append(tok)
      if DEBUG:
        print('Append to queue 1')
        show(queue)
    else:
      if prev == '(':
        var = tok
        if DEBUG:
          print('New var')
      elif prev == '/':
        concept = tok
        var_concept[var] = concept
        nn = Node(var, concept)
        stack.append(nn)
        queue.append(concept)
        if DEBUG:
          print('Put to stack, append to queue 2')
          show(queue)
      elif prev.startswith(':'):
        if tok in var_concept:
          concept = var_concept[tok]
          queue.append(concept)
          queue.append(concept)
          if DEBUG:
            show(queue)
            print('Append to queue 2')
        else:
          constant = tok
          queue.append(constant)
          queue.append(constant)
          if DEBUG:
            show(queue)
            print('Append to queue 3')
    prev = tok

  return ' '.join(queue)


def show(queue):
  print(' '.join(queue))


def node_of(concept_var, new_concept):
  prefix = new_concept[0]
  chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
  if DEBUG:
    print('-> ' + new_concept)
  if prefix not in chars:
    prefix = 'x'
  if new_concept in concept_var:
    node = Node(concept_var[new_concept], new_concept)
    return node, True
  else:
    vars = concept_var.values()
    idx = 0
    v = prefix + str(idx)
    while v in vars:
      idx += 1
      v = prefix + str(idx)
    concept_var[new_concept] = v
    node = Node(v, new_concept)
    return node, False


def new_line(ntab, node, rel=None, node_exist=False):
  line = ''
  for i in range(ntab):
    line += '\t'
  if rel:
    if rel == ':quant':
      line += '%s %s' % (rel, node.concept)
      return line
    else:
      line += '%s ' % rel
  if node_exist:
    line += node.var
  else:
    line += '(%s / %s' % (node.var, node.concept)
  return line


def delinearize(linearized_amr):
  lines = []
  tokens = linearized_amr.split(' ')
  stack = []
  concept_var = {}
  rel = None
  line = ''

  for tok in tokens:
    if tok.startswith(':'):
      rel = tok
    else:
      if len(stack) > 0:
        top = stack[-1]
        if tok == top.concept:
          stack.pop()
          if not top.is_constant:
            line += ')'
          if len(stack) ==0:
            break
          continue
      if len(line) > 0:
        lines.append(line)
      node, exist = node_of(concept_var, tok)
      if rel == ':quant' or exist:
        node.is_constant = True
      line = new_line(len(stack), node, rel=rel, node_exist=exist)
      rel = None
      stack.append(node)
  lines.append(line)
  return lines


def delinearize2(linearized_amr):
  lines = []
  tokens = linearized_amr.split(' ')
  stack = []
  concept_var = {}
  rel = None
  line = ''

  for tok in tokens:
    if tok.startswith(':'):
      if rel == None:
        rel = tok
      else:
        break
    else:
      if len(stack) > 0:
        top = stack[-1]
        if tok == top.concept:
          stack.pop()
          if not top.is_constant:
            line += ')'
          if len(stack) ==0:
            break
          continue
      if len(line) > 0:
        lines.append(line)
      node, exist = node_of(concept_var, tok)
      if rel == ':quant' or exist:
        node.is_constant = True
      line = new_line(len(stack), node, rel=rel, node_exist=exist)
      rel = None
      stack.append(node)
  for x in stack:
    line += ')'
  lines.append(line)
  return lines

def test():
  with open('../tmp/sample.amr.txt') as f:
    lines = f.readlines()

  for line in lines:
    print(line, end='')
  print('------------------')
  amr = linearize(lines[3:])
  print(amr)

  # amr = 'establish-01 :ARG1 model :mod innovate-01 :ARG1 industry industry innovate-01 model
  # establish-01'
  lines = delinearize2(amr)
  for line in lines:
    print(line)


if __name__ == '__main__':
  test()
