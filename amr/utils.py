import codecs


def read_amr_format(path, return_dict=True, filter_length=-1):
  '''
  This function read a amr file format (both the amr and the jpc-rre conll format.
  :param path: the AMR file
  :return: return a dictionary which:
              key is the sentence id
              value is a dictionary of id, snt, doc (doc is a list of string which is a line)
  '''
  with codecs.open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
  data = []
  sample = {}
  doc = []
  nodes = []
  edges = []
  root = ''
  for line_number, l in enumerate(lines):
    line = l.strip()
    if len(line) > 2:
      if line[0] == '#':
        if line[4:8] == 'node':
          nodes.append(line[9:])
        elif line[4:8] == 'edge':
          edges.append(line[9:])
        elif line[4:8] == 'root':
          root = line[9:]
        else:
          tag = line.split(' ')[1][2:]
          start = 4 + len(tag) + 1
          sample[tag] = line[start:]
      else:
        doc.append(l)
    else:
      if 'id' in sample.keys() and 'snt' in sample.keys():
        snt_length = len(sample['snt'].split(' '))
        if len(doc) > 0 and snt_length > filter_length:
          sample['doc'] = doc
          sample['root'] = root
          if len(nodes) > 0:
            sample['nodes'] = nodes
          sample['edges'] = edges
          if len(root) > 0:
            sample['root'] = root
          data.append(sample)
        else:
          print('Ignore document %s' % (sample['id']))
      doc = []
      root = ''
      edges = []
      nodes = []
      sample = {}
  if 'id' in sample.keys() and 'snt' in sample.keys():
    snt_length = len(sample['snt'].split(' '))
    if len(doc) > 0 and snt_length > filter_length:
      sample['doc'] = doc
      if len(nodes) > 0:
        sample['nodes'] = nodes
      sample['edges'] = edges
      if len(root) > 0:
        sample['root'] = root
      data.append(sample)
    else:
      print('Ignore document %s' % (sample['id']))
  else:
    print('[Error] Read AMR error at line %d/%d, '
          'no "id" or "snt" attribute' % (line_number, len(lines)))
  return data


def save_amr_format(amrobj_list, path, end='\n'):
  f = codecs.open(path, 'w', encoding='utf-8')
  for amr in amrobj_list:
    doc = end.join(amr['doc'])
    text = '# ::id %s\n' \
           '# ::snt %s\n' \
           '%s\n\n' % (amr['id'], amr['snt'], doc)
    f.write(text)
  f.close()
