import math
import string
import pickle
from nltk.corpus import brown

def ngrams_freq(text,ngram_len):
    '''
	ngram_len : integer (length of the ngrams whose freq is needed)
	text : string (corpus in lowercase, continous text)
	returns a dict with letter:freq as iteritems
    '''
    ngrams_dict = dict()
    for j in range(len(text) - ngram_len + 1):
        temp = text[j:j + ngram_len]
	if temp in ngrams_dict:
		ngrams_dict[temp] +=1
	else:
		ngrams_dict[temp] =1
    with open('ngram_dict_'+str(ngram_len),'wb') as f:
	pickle.dump(ngrams_dict,f)

    return ngrams_dict

##########################################################################

def corpusDL(corpus,freq):
    '''
        calculates and returns the DL of the corpus using freq
	freq : dict for the letters and their frequency
	corpus: space removed continuous text in lowercase
    '''
   
    X = len(corpus)
    DL =0
    for key,value in freq.iteritems():
	DL += value * (math.log(value,2) - math.log(X,2))
	#if key == 'e' or key =='s':
	#    print key ,' in original corpus occurs ', str(value),' times and code length is ',str(math.log(value,2) - math.log(X,2))
    DL = -1*DL
    print 'DL is ',str(DL), ' Maximum DLG will be ',str(DL - (((X*1.0)/30)*math.log(30,2)))
    return DL

##########################################################################

def occurrences(sentence,substring):
    return sentence.count(substring)

##########################################################################


def increase_DELIM(corpus,DELIM,INC):
	''' takes the corpus and replaces all occurrences of DELIM character multiplied by INC.
	corpus : continuous text (string)
	DELIM : a single delimiter character
	INC : an integer that tells the length of the resulting corpus 
	'''
	INC_DELIM = INC*DELIM
	corpus = corpus.replace(DELIM,INC_DELIM)

	return corpus

##############################################################################33
def load_corpus(fname,delimiter):
	''' takes the filename in which space separated text is located 
	and returns as the continous text in lowercase and spaces replaced by underscores
        fname : file name as string
	'''

	data = ''
	#punctuation ='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
	

	if fname == 'BROWN':
		words = brown.words()
		text = ' '.join(words)
		text = text.lower()
		text = text.strip()
#    		for punc in punctuation:
#			text = text.replace(punc,' ')
    		text = text.replace('  ',' ')
		text = text.replace('  ',' ')
		text = text.replace('  ',' ')
		text = text.replace(' ',delimiter)
		data = text
	else:
		with open(fname,'r') as f:
			file_text = f.readlines()

		for line in file_text:
			text = line.lower()
			text = text.strip()
#    		for punc in punctuation:
#			text = text.replace(punc,' ')
    			text = text.replace('  ',' ')
			text = text.replace('  ',' ')
			text = text.replace('  ',' ')
			text = text.replace(' ',delimiter)
			data += text


	return data
	
##########################################################################

def strip_punc(corpus):
    ''' uses the string.punctuation to remove all punc
	symbols from the corpus
	corpus : string - continuous text in lowercase
	string.punc = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    '''
	
    for punc in string.punctuation:
	corpus = corpus.replace(punc,'')
     
    return corpus
 
##########################################################################

def load_vocab(fname):
    ''' takes the file name as input and forms the vocab list
	after convertring to lowercase and  removing punctuations
	fname : string
	returns a dict containing words and frequency
    '''
    vocab ={}
    punctuation ='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
    with open(fname,'r') as f:
	for line in f:
	    text = line.lower()
	    for punc in punctuation:
		text = text.replace(punc,' ')
	    text = text.replace('  ',' ')
	    text = text.replace('  ',' ')
	    text = text.split(' ')
            for word in text:
		count = vocab.get(word,0) + 1
		vocab[word] = count
    return vocab

###########################################################################

def calc_precision_words(vocab,output):
    ''' takes the original vocabulary of the input file as a dict containing
	(word,freq) and the output as a list  of segments
	calculates the word wise precision and prints it
	vocab : dict
	output: list
    '''


    correct =0
    total = 0
    for word in output:
	word = word.replace('_','')
	if len(word)>0:
	    if word in vocab.keys():
	        correct+=1

	    total+=1

    recall_base = 0
    for segment in vocab.keys():
	recall_base += vocab[segment]
    
    s1= 'Precision is '+str((correct*1.)/total)		#relevant segments / total number of segments in output
    s2= 'Recall is '+str((correct*1.)/recall_base)	#relevant segments / actual number of segments as in input
   
    with open('precision_word.txt','a') as f:
	f.write(s1+'\n')
	f.write(s2+'\n')

######################################################################################################
def calc_precision_boundaries_strict(vocab,output,boundaries):
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


	s1= 'precision wrt word boundaries (strict) is '+str(correct*1.0/total)+ ' correct = '+str(correct)+' output len : '+str(total)
	s2= 'Recall wrt boundaries (strict) is ' + str(correct*1.0/len(boundaries))+ ' correct = '+str(correct)+' boundaries : '+str(len(boundaries))	

	with open('precision_strict.txt','a') as f:
		f.write(s1+'\n')
		f.write(s2+'\n')

######################################################################################################
def calc_precision_boundaries_relaxed(vocab,output,boundaries):
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
			key =index
			if key in boundaries:
				correct+=1
			#print key, (key in boundaries)
			index+=length


	s1= 'precision wrt word boundaries (relaxed) is '+str(correct*1.0/total)+ ' correct = '+str(correct)+' output len : '+str(total)
	s2= 'Recall wrt boundaries (relaxed) is ' + str(correct*1.0/len(boundaries))+ ' correct = '+str(correct)+' boundaries : '+str(len(boundaries))	

	with open('precision_relaxed.txt','a') as f:
		f.write(s1+'\n')
		f.write(s2+'\n')
#######################################################################################################
def form_vocab(corpus,DELIM):
	''' takes the file name as input and forms the vocab list
	by splitting on underscores
	corpus : continous text (string)
	returns a dict containing words and frequency
	'''

	vocab ={}
	words = corpus.split(DELIM)
	for word in words:
		count = vocab.get(word,0) + 1
		vocab[word] = count
	#print vocab
        return vocab


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

##########################################################################################################

def form_boundaries_strict(corpus,DELIM):
	'''takes the '_' separated text and forms a set with start position and length
	of segment as an element
	'''

	boundaries = set()
	index = 0
	words = corpus.split(DELIM)
	for word in words:
		length = len(word)
		boundaries.add((index,length))
		index+=length

	#print boundaries
	return boundaries


def form_boundaries_relaxed(corpus,DELIM):
	''' takes the corpus separated by DELIM as delimiter between words . Returns the indices of all boundaries
	'''
	boundaries = set()
	index = 0
	words = corpus.split(DELIM)
	for word in words:
		length = len(word)
		boundaries.add(index)
		index+=length

	#print boundaries
	return boundaries
		
