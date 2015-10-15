from nltk.stem.lancaster import LancasterStemmer
from stemmer import syllabify
import pickle


f_names = {'alice.txt'}
stemmer = syllabify()

syllables = pickle.load(open('syllable_dict','rb'))

for fname in f_names:
	text = ""	
	with open(fname,'r') as f:
		data = f.readlines()
		print len(data)
		if type(data)==list and len(data)==1:
			data = data[0]
		elif len(data)>1:
			data = ' '.join(data)

		data = data.split(' ')

	for word in data:
		word = word.lower()
		if word in syllables:
			word = syllables[word]
		else:
			s_word=stemmer.stemmed(word)
			if s_word != word and s_word in syllables:
				word = syllables[s_word]+'#'+word[-1*len(s_word)]
			
		text+=' '+word

	
	with open('mod_'+fname,'w') as f:
		f.writelines(text)
