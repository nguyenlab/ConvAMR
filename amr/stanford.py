stanford_server_ip = '150.65.242.105'
stanford_server_port = '9000'
stanford_server_url = 'http://%s:%s' % (stanford_server_ip, stanford_server_port)


verbose = 1

class StanfordServerRequest(object):
  def __init__(self):
    if verbose > 0:  # info
      print('Stanford server at: %s' % stanford_server_url)
    self.result = None

  def request(self, sent):
    properties = {"annotators": "tokenize,pos,ner",
                  "outputFormat": "json"}
    response = requests.post(URL, sent, json=properties)
    json_obj = response.json()
    # if verbose > 1:  # debug
    #   print(json_obj)
    return json_obj