import pickle

f=open('border_dict','rb')

border_dict = pickle.load(f)

cutoff = 0.99

borders = []

for key in border_dict:
#	if key == 'dj':
#		print border_dict[key]
	if border_dict[key] > cutoff:
		borders.append(key)

with open('borders.txt','w') as f:
	for key in borders:
		f.write(key+'\n')
