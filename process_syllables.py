import pickle
syllables = dict()

with open('Syllables.txt','r') as f:
	data = f.readlines()
	for row in data:
		row = row.split('=')
		word = row[0]
		syl = (row[1].rstrip()).split('\xb7')
		syllables[word]='#'.join(syl)

with open('SyllablesUpdate.txt','r') as f:
	data = f.readlines()
	for row in data:
		if row == '\r\n':
			continue
		row = row.rstrip()
		row = row.split('=')
		print row
		
		word =row[0]
		
		syl = (row[1].rstrip()).split(' ')
		if word in syllables:
			print word ,' is already present ',syl,'   ',syllables[word]
		else:
			syllables[word] = '#'.join(syl)

#print syllables['welcome']
f=open('syllable_dict','wb')
pickle.dump(syllables,f)
f.close()
