import copy
from helpers import *
from ViterbiSeg import *
  

def main():
	SAMPLE_start = 0
	SAMPLE_end = 100
	f_names = ['BROWN']
	#f_names =['BROWN','coffee.txt','editorial.txt','news_brown.txt', 'webtext_nltk.txt','alice.txt','brown_religion.txt']
        
        DELIM = '_'
	delim_len = 0

	for fname in f_names:
		corpus = load_corpus(fname,DELIM) #load corpus with space replaced by underscores,lowercase and all punc removed
		text = corpus[SAMPLE_start:SAMPLE_end]

		vocab = form_vocab(text,DELIM) #number of unique words	vocab is a dict
		boundaries_strict = form_boundaries_strict(text,DELIM)
		boundaries_relaxed = form_boundaries_relaxed(text,DELIM)

		corpus = increase_DELIM(corpus,DELIM,delim_len)
		text = increase_DELIM(text,DELIM,delim_len)

		print fname  + " corpus size : "+str(len(corpus))
		#print 'SAMPLE size ',str(SAMPLE)
		
		#for ngram_len in range(11,26):
	   	#	ngrams_freq(corpus,ngram_len)	

		freq = ngrams_freq(corpus,1)
	        DL = corpusDL(corpus,freq)
		output= OpSeg(corpus,freq,DL,text)
		with open('out_'+fname,'w') as f:
			for word in output:
				f.write(word+ '  ')
		
		with open('precision_strict.txt','a') as f:
			f.write(fname+'\n')
		
		with open('precision_relaxed.txt','a') as f:
			f.write(fname+'\n')
	
		with open('precision_word.txt','a') as f:
			f.write(fname+'\n')

		calc_precision_boundaries_strict(vocab,output,boundaries_strict)
		calc_precision_boundaries_relaxed(vocab,output,boundaries_relaxed)
		calc_precision_words(vocab,output)
		


if __name__ == '__main__':

	
	main()
