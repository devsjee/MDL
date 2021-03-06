import copy
from helpers import *
from nltk.corpus import brown

global INC_DELIM 
DELIM = '_'
SAMPLE = 2060


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
	file_text = None
	#punctuation ='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
	
	if fname == 'BROWN':
		words = brown.words()
		file_text = ' '.join(words)
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



def calc_new_DL(unigram_freq,substr,substr_freq,new_corpus_len):
    new_DL = 0
    for unigram,freq in unigram_freq.iteritems():
        substr_key_freq = occurrences(substr,unigram)
        #print '{} with freq {} occurs {} times in {}'.format(key,value,csx,s)
        new_freq = freq - substr_freq*substr_key_freq + substr_key_freq 
	#print 'value ',value,'cs ',cs,'csx',csx,'n ',n;
	new_DL += new_freq * (math.log(new_freq,2) -math.log(1.0*new_corpus_len,2))
    
    new_DL += substr_freq* (math.log(substr_freq,2) - math.log(new_corpus_len,2))
    new_DL = -1*new_DL
    return new_DL

def print_details(unigram_freq,substr,substr_freq,new_corpus_len,corpus_len,DL):
    new_DL = 0
    old_DL=0
    new_DL_t =0
    old_DL_t=0

    for unigram,freq in unigram_freq.iteritems():
        substr_key_freq = occurrences(substr,unigram)
        print '{} with freq {} occurs {} times in {}'.format(unigram,freq,substr_key_freq,substr)
        new_freq = freq - substr_freq*substr_key_freq + substr_key_freq 
	print 'new frequency is '+str(new_freq)
	print 'new bitlength is'+str( new_freq * (math.log((new_freq/(1.0*new_corpus_len)),2)))
	print 'old bitlength is'+str( freq * (math.log((freq/(1.0*corpus_len)),2)))

	if unigram not in substr:
	    old_DL += freq*(math.log((freq/(1.0*corpus_len)),2))
	    new_DL += new_freq * (math.log(new_freq,2) -math.log(1.0*new_corpus_len,2))
	else:
	    old_DL_t += freq*(math.log((freq/(1.0*corpus_len)),2))
	    new_DL_t += new_freq * (math.log(new_freq,2) -math.log(1.0*new_corpus_len,2))
    print 'DL : '+str(DL)+'. original DL due to other chars : '+str(abs(old_DL))+'. change in DL due to other chars : '+ str(abs(new_DL))
    print 'original DL due to constituent chars : '+str(abs(old_DL_t))+'. change in DL due to constituent chars : '+ str(abs(new_DL_t))
    print 'DL due to substring is '+ str(abs(substr_freq* (math.log(substr_freq,2) - math.log(new_corpus_len,2))))
    print substr+' occurs '+ str(substr_freq) + ' times. corpus len new = '+ str(new_corpus_len)+' . prob is '+str(substr_freq/(1.0*new_corpus_len))
    print 'new DL is '+str( calc_new_DL(unigram_freq,substr,substr_freq,new_corpus_len))
    
    

def DLG(corpus,unigram_freq,DL,substr):
    ''' calculates the gain in description length brought about by 
	a sequence s
	freq : dict containing the frequency of unigrams
	text : space removed continous corpus text in lowercase
	s    : the subsequence
    '''
    corpus_len = len(corpus)
    substr_len = len(substr)
	
    ### added on 08-09-15 to include the constraint that a valid English word will have atleast one syllable with one nuclues
    #flag = False
    vowels = ['a','e','i','o','u','_']
    #for character in substr:
	#if character in vowels:
	    #flag = True
	    #break

    #if flag == False:
        #print 'DLG of {} is {}'.format(substr,-1000)
	#return -1000
    ### penalty is incurred if this constraint is not met. Constraint ends with this comment

    if substr_len == 1:
        return 0
	
    if substr_len == 3 and substr[-2:]=='le' :
	#print 'Illegal segment ending in le ',substr
	return -1000

    #if substr[0:2] in {'db','km','lp','mp','ns','ms','td','kd','md','ld','bd','cd','fd','gd','hd','jd','nd','pd','qd','rd','sd','vd','wd','xd','yd','zd'}:
	#print 'Illegal onset ',substr
	#return -1000
	
    '''if substr_len > 3:
	flag = False
	for c in substr[0:3]:
	    if c in vowels:
		flag = True			
		break
	if flag == False:
	    if substr[0] == 's':	
		flag = True

	if flag == False:
	    print 'Beginning with three consonants : ',substr
	    return -1000'''
		
	

    substr_freq = occurrences(corpus,substr)
    new_corpus_len = corpus_len - substr_freq*substr_len + substr_freq + substr_len + 1
    #print s+' occurs '+ str(cs) + ' times'
    
    new_DL = calc_new_DL(unigram_freq,substr,substr_freq,new_corpus_len)
    dlg = (DL - new_DL) /substr_freq
    #print 'DLG of {} is {}'.format(substr,dlg)
   
    #if dlg>0:
	#print_details(unigram_freq,substr,substr_freq,new_corpus_len,corpus_len,DL)
	#pause = raw_input('')

    #for suffix in {'ed','edly','ible','able','ing','abled','ingly','ary','rily','tion','ian','ous','ckle'}:
	#if substr.endswith(suffix):	
	   # return dlg+1000
	

    return dlg*1.0/DL

def OpSeg(corpus,unigram_freq,DL,text):
    n = len(text)
    OS = []
    DLG_stored = []

    for k in range(0,n):
	if k>30:
	    OS[k-30][:]=[]

        OS.append([])
        if k>0:
            OS[k][:]= []
	    OS[k] = copy.deepcopy(OS[k-1])
	    OS[k].append(text[k])
	    DLG_stored.append(DLG_stored[k-1])
	else:
	    OS[k][:]=[]
	    OS[k].append(text[k])
	    DLG_stored.append(0)

        '''print 'k value is ',k
        print 'OS is ', OS
        print 'DLG stored is ',DLG_stored'''

	for j in range(k,-1,-1):
	    if j < k-25:
	        break
	
	    ngram = text[j:k+1]
	    #print 'ngram value from ',j,' to ',k+1,' is ',ngram
	    if occurrences(corpus,ngram)<2:
	        break
	    #if len(ngram) == 1 :		#commented to include constraint
	    #    dlgain = DLG_stored[j-1]
            if j>0:
	        dlgain = DLG_stored[j-1] + DLG(corpus,unigram_freq,DL,ngram)
	    else:
		dlgain = DLG(corpus,unigram_freq,DL,ngram)

	    '''print DLG_stored
            print 'new DL', dlgain
            print 'DLG_stored is ',DLG_stored[k]'''
	    if (dlgain > DLG_stored[k]) and j>0:
	        OS[k][:] = []
                OS[k] = copy.deepcopy(OS[j-1])
	        OS[k].append(ngram)
		#print 'ngram is ',ngram
                DLG_stored[k] = copy.deepcopy(dlgain)
                print 'OS[{}] is now assigned with dlgain {}'.format(k,DLG_stored[k])
	    elif (dlgain > DLG_stored[k]) and j==0:
		OS[k][:]=[]
		OS[k].append(ngram)
		DLG_stored[k] = copy.deepcopy(dlgain)
                print 'OS[{}] is now assigned with dlgain {}'.format(k,DLG_stored[k])
    return OS[n-1]


def main():
	global SAMPLE
	f_names =['biotext.txt']
	#f_names =['alice.txt','coffee.txt','editorial.txt','news_brown.txt', 'webtext_nltk.txt','alice.txt','brown_religion.txt']


	for fname in f_names:
		corpus = load_corpus(fname) #load corpus with space replaced by underscores,lowercase and all punc removed
		text = corpus[0:SAMPLE]

		#vocab = form_vocab(text) #number of unique words	vocab is a dict
		#word_boundaries = form_boundaries(text)

		#corpus = include_DELIM(corpus)
		#text = include_DELIM(text)

		print fname  + " corpus size : "+str(len(corpus))
		
		freq = ngrams_freq(corpus,1)
	        DL = corpusDL(corpus,freq)
		output= OpSeg(corpus,freq,DL,text)
		with open('BIO_out_'+str(len(INC_DELIM))+'_'+fname,'w') as f:
			for word in output:
				f.write(word+ '  ')
		
		'''with open('precision.txt','a') as f:
			f.write(fname+'\n')
		calc_precision(vocab,output,word_boundaries)
		'''
		
		print

if __name__ == '__main__':

	
	for i in range(0,1):
		INC_DELIM = '_'
		INC_DELIM *= i	
		main()

