import math
import string


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


def load_corpus(fname):
    ''' takes the filename in which space separated text is located 
	and returns as the continous text in lowercase
        fname : file name as string
    '''
    data = ''
    with open(fname,'r') as f:
	for line in f:
	    data+= str(line.strip())

    data = data.lower()
    data = data.replace(' ','')
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

def calc_precision(vocab,output):
    ''' takes the original vocabulary of the input file as a dict containing
	(word,freq) and the output as a list  of segments
	calculates the word wise precision and prints it
	vocab : dict
	output: list
    '''
    graph = []
    new_vocab = {}
  

    for word in output:
	count = new_vocab.get(word,0)+1
	new_vocab[word] = count
    with open('analyse','w') as f:
	for word,count in vocab.iteritems():
            f.write(word + '\t\t'+ str(count)+ '\t'+ str(new_vocab.get(word,0)) + '\n')
	    graph.append((count,new_vocab.get(word,0)))

    with open('output.txt','w') as f:
	for word,count in new_vocab.iteritems():
            f.write(word + '\t\t'+ str(count) + '\n')
	
    f=open('graph.txt','w')
    for line in graph:
	f.write(str(line[0])+ ' '+ str(line[1])+ '\n')

    correct =0
    total = 0
    for word in output:
	word = word.replace('_','')
	if len(word)>0:
	    if word in vocab.keys():
	        correct+=1
	    total+=1

    print 'Precision is '+str((correct*1.)/total)
	
    f.close()
