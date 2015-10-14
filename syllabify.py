from nltk.stem.lancaster import LancasterStemmer


class syllabify():


	def __init__(self,word):
	
		stemmed_word=self.stemmed(word)
		print 'stemmed word is ',stemmed_word
		stemmed_length = len(stemmed_word)

		stem = len(word)-stemmed_length

		if stem >0:
			word = self.parse(stemmed_word)+'_'+word[-1*stem:]
		else:
			word = self.parse(word)
		
		print word

	def stemmed(self,word):
		stemmer = LancasterStemmer()
		return stemmer.stem(word)

	def parse(self,word):
		vowels = {'a','e','i','o','u'}
		diphthongs = {'th','sh','ph','th','ch','wh'}
		t_word = word	

		w_index =0
		for i in range(len(t_word)):
			if t_word[i] in vowels:
				if i ==0:
					continue
				else:
					index = -1
					for j in range(w_index-1,-1,-1):
						if word[j] in vowels:
							index=j
							break
					if index >= 0:
						word = word[0:index+1]+'_'+word[index+1:]
						w_index+=1
			w_index+=1

		return word


