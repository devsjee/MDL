from nltk.stem.lancaster import LancasterStemmer



class syllabify():


	def __init__(self,word):
	
		stemmed_word=self.stemmed(word)
		print 'stemmed word is ',stemmed_word
		stemmed_length = len(stemmed_word)

		stem = len(word)-stemmed_length

		#if stem >0:
		#	word = self.parse(stemmed_word)+'_'+word[-1*stem:]
		#else:
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
			if i == len(t_word)-1 and t_word[i]=='e':
				word = word[:-3]+'_'+word[-3:]
				break

			if t_word[i] in vowels:
				if i ==0:
					w_index+=1
					continue
				elif t_word[i+1] in vowels:
					w_index+=1
					continue
				elif i<len(t_word)-3 and t_word[i+1] not in vowels and t_word[i+2] not in vowels and t_word[i+3] in vowels:
					word = word[:w_index+2]+'_'+word[w_index+2:]
					i=i+4
					w_index+=5
				else:
					index = -1
					for j in range(w_index-2,-1,-1):
						if word[j] in vowels:
							index=j
							break
					if index >= 0:
						word = word[0:index+1]+'_'+word[index+1:]
						w_index+=1
			w_index+=1

		return word

syllabify('approach')
