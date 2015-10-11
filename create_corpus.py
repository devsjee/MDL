import mainDLG

global INC_DELIM 
DELIM = '_'
SAMPLE = 30000


def sort(vocab):
	vocab_list =[]
	for key in vocab:
		vocab_list.append((key,vocab[key]))
	vocab_list.sort(key= lambda x:x[1],reverse =True)
	
	print 'returning sorted vocab list..'
	return vocab_list

def write_vocab(vocab,fname):
	with open(fname,'w') as f:
		for item in vocab:
			f.writelines(item[0]+", "+str(item[1])+"\n")

	print 'done writing vocab to file'


def trim(vocab,freq):
	'''	takes the vocab list and returns the vocab with keys of frequency above 'freq' only
	'''
	temp = []
	for item in vocab:
		if item[1] >freq:
			temp.append(item)
	return temp


def contribution(vocab):
	size = 0
	for item in vocab:
		size+= len(item[0])*item[1]
	return size

def load_corpus(fname):
	''' takes the filename in which space separated text is located 
	and returns as the continous text in lowercase and spaces replaced by underscores
        fname : file name as string
	'''
	global DELIM
	data = ''
	#punctuation ='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
	with open(fname,'r') as f:
		for line in f:
			text = line.lower()
			text = text.strip()
#	    		for punc in punctuation:
#				text = text.replace(punc,' ')
	    		text = text.replace('  ',' ')
			text = text.replace('  ',' ')
			text = text.replace('  ',' ')
			text = text.replace(' ','_')
			data += text

	return data
	

def form_vocab(corpus):
	''' takes the file name as input and forms the vocab list
	by splitting on underscores
	corpus : contunoues text (string)
	returns a dict containing words and frequency
	'''

	
	vocab ={}
	words = corpus.split(DELIM)
	for word in words:
		count = vocab.get(word,0) + 1
		vocab[word] = count
	#print vocab
        return vocab
	
	
def form_boundaries(corpus):
	'''takes the '_' separated text and forms a set with start position and length
	of segment as an element
	'''
	global DELIM
	boundaries = set()
	index = 0
	words = corpus.split(DELIM)
	for word in words:
		length = len(word)
		boundaries.add((index,length))
		index+=length

	#print boundaries
	return boundaries
		
def calc_precision(vocab,output,boundaries):
	''' output : list format
	if a segment is present in boundaries,it is counted as correct.
	to check if its present, we form an element with starting position and 
	length of segment as a tuple
	'''
	correct = 0
	total = 0	
	index = 0
	flag = False

	for word in output:

		word = word.replace('_','')
		length = len(word)
		if length > 0:
			total+=1
			key =(index,length)
			if key in boundaries:
				correct+=1
			#print key, (key in boundaries)
			index+=length


	s1= 'precision wrt word boundaries is '+str(correct*1.0/total)+ ' correct = '+str(correct)+' output len : '+str(total)
	s2= 'Recall wrt boundaries is ' + str(correct*1.0/len(boundaries))+ ' correct = '+str(correct)+' boundaries : '+str(len(boundaries))	

	with open('precision.txt','a') as f:
		f.write(s1+'\n')
		f.write(s2+'\n')

def include_DELIM(corpus):
	''' takes the corpus and removes all occurrences of DELIM character and returns it
	corpus : continous text (string)
	'''
	global INC_DELIM
	corpus = corpus.replace('_',INC_DELIM)

	return corpus

def pre_calc_recall(output):
	output_segment = set()
	for segment in output:
		output_segment.add(segment)
	return output_segment

def calc_recall(output_segment,vocab,threshold):
	recall = 0
	
	if type(vocab) == list:
		vocab_new = [x[0] for x in vocab]
	else:
		vocab_new = vocab

	for segment in output_segment:
		if segment in vocab_new:
			recall+=1
		
	print 'percentage of vocab recalled with threshold '+ str(threshold)+ ' is '+str(recall*1.0 /len(vocab))



def main():
	global SAMPLE
	f_names =['alice.txt']
	#f_names =['coffee.txt','editorial.txt','news_brown.txt', 'webtext_nltk.txt','alice.txt','brown_religion.txt']


	for fname in f_names:
		corpus = load_corpus(fname) #load corpus with space replaced by underscores,lowercase and all punc removed

		text = corpus[0:SAMPLE]

		vocab = form_vocab(text) #number of unique words	vocab is a dict
		word_boundaries = form_boundaries(text)

		corpus = include_DELIM(corpus)
		text = include_DELIM(text)

		print fname  + " corpus size : "+str(len(corpus))
		
		freq = mainDLG.ngrams_freq(corpus,1)
	        DL = mainDLG.corpusDL(corpus,freq)
		output= mainDLG.OpSeg(corpus,freq,DL,text)
		with open('c2_output_'+str(len(INC_DELIM))+'_'+fname,'w') as f:
			for word in output:
				f.write(word+ '  ')
		
		with open('precision.txt','a') as f:
			f.write(fname+'\n')
		calc_precision(vocab,output,word_boundaries)
		mainDLG.calc_precision(vocab,output)
		
		print

if __name__ == '__main__':

	
	for i in range(0,1):
		INC_DELIM = '_'
		INC_DELIM *= i	
		main()
