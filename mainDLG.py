import copy
from helpers import *

F_NAME = 'brown_religion.txt'

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

    if substr_len == 1:
        return 0
    substr_freq = occurrences(corpus,substr)
    new_corpus_len = corpus_len - substr_freq*substr_len + substr_freq + substr_len + 1
    #print s+' occurs '+ str(cs) + ' times'
    
    new_DL = calc_new_DL(unigram_freq,substr,substr_freq,new_corpus_len)
    dlg = (DL - new_DL) /substr_freq
    #print 'DLG of {} is {}'.format(substr,dlg)
   
    #if dlg>0:
	#print_details(unigram_freq,substr,substr_freq,new_corpus_len,corpus_len,DL)
	#pause = raw_input('')
    return dlg    


def OpSeg(corpus,unigram_freq,DL,text):
    n = len(text)
    OS = []
    DLG_stored = []

    for k in range(0,n):
	if k>25:
	    OS[k-25][:]=[]

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

	for j in range(k-1,-1,-1):
	    if j < k-20:
	        break
	
	    ngram = text[j:k+1]
	    #print 'ngram value from ',j,' to ',k+1,' is ',ngram
	    if occurrences(corpus,ngram)<2:
	        break
	    if len(ngram) == 1 :
	        dlgain = DLG_stored[j-1]
            elif j>0:
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
                #print 'OS[{}] is now assigned with dlgain {}'.format(k,DLG_stored[k])
	    elif (dlgain > DLG_stored[k]) and j==0:
		OS[k][:]=[]
		OS[k].append(ngram)
		DLG_stored[k] = copy.deepcopy(dlgain)
                #print 'OS[{}] is now assigned with dlgain {}'.format(k,DLG_stored[k])
    return OS[n-1]


def main(fname):
    vocab = load_vocab(fname)
    print 'len of vocab (number of unique words) is '+ str(len(vocab.keys()))

    corpus = load_corpus(fname)
    corpus = strip_punc(corpus)
    print 'len of corpus (number of characters) is '+str(len(corpus))

    freq = ngrams_freq(corpus,1)
    DL = corpusDL(corpus,freq)

    output= OpSeg(corpus,freq,DL,corpus[3000:6000])
    print output
    calc_precision(vocab,output)
  


if __name__ == '__main__':
    main(F_NAME)