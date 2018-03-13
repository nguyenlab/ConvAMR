
import os
import codecs
import arm.utils as utils





def split_long_short(file_paths, prefix = 'default', threshhold=20):
	data = []
	for file in file_paths:
		data.append(utils.read_amr_format(file))

	short_data, long_data = [], []

	for d in data:
		if (d['text'].split(' ') )>threshhold:
			long_data.append(d)
		else:
			short_data.append(d)
	utils.save_amr_format(short_data, 'tmp/%s.short_data.amr.txt'%(prefix))
	utils.save_amr_format(long_data, 'tmp/%s.long_data.amr.txt'%(prefix))

if __name__ == '__main__':
	files = []
	split_long_short(files, 'LDC2014T12')
	files = []
	split_long_short(files, 'civilcode')
	