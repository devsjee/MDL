import copy
from helpers import occurrences
import math

def lexical_quality(substr):
	### added on 08-09-15 to include the constraint that a valid English word will have atleast one syllable with one nuclues
    substr_len = len(substr)

    vowels = ['a','e','i','o','u']
    v_count = 0

    if substr_len == 1 :
	return -1000

    for character in substr:
	if character in vowels:
	    v_count+=1

    if v_count ==0 and substr != 'by':
        #print 'DLG of {} is {}'.format(substr,-1000)
	return -1000
    
	
    if substr_len == 3 and substr[-2:]=='le' :
	#print 'Illegal segment ending in le ',substr
	return -1000

    if substr[0:2] in {'db','km','lp','mp','ns','ms','td','kd','md','ld','bd','cd','fd','gd','hd','jd','nd','pd','qd','rd','sd','vd','wd','xd','yd','zd'}:
	#print 'Illegal onset ',substr
	return -1000
	
    if substr_len > 3:
	flag = False
	for c in substr[0:3]:
	    if c in vowels:
		flag = True			
		break
	if flag == False:
	    if substr[0] == 's':	
		flag = True

	if flag == False:
	    #print 'Beginning with three consonants : ',substr
	    return -1000


    return 1

	
def calc_new_DL(unigram_freq,substr,substr_freq,new_corpus_len):
    new_DL = 0
    for unigram,freq in unigram_freq.iteritems():
        substr_key_freq = occurrences(substr,unigram)
        #print '{} with freq {} occurs {} times in {}'.format(key,value,csx,s)
        new_freq = freq - substr_freq*substr_key_freq + substr_key_freq 
	#print 'value ',value,'cs ',cs,'csx',csx,'n ',n;
	new_DL += new_freq * (math.log(new_freq,2) -math.log(1.0*new_corpus_len,2))
	#if unigram == 's' or unigram == 'e':
	#    print 'freq of ',unigram,' is ',str(new_freq),'; code length is ',str(math.log(new_freq,2) -math.log(1.0*new_corpus_len,2))
		

    #print 'new_DL for unigrams only ',str(-1*new_DL)
    #print 'code length is ',str(math.log(substr_freq,2) - math.log(1.0*new_corpus_len,2))
    new_DL += substr_freq* (math.log(substr_freq,2) - math.log(1.0*new_corpus_len,2))
    new_DL = -1*new_DL
    return new_DL


def DLG(corpus,unigram_freq,DL,substr):
    ''' calculates the gain in description length brought about by 
	a sequence s
	freq : dict containing the frequency of unigrams
	text : space removed continous corpus text in lowercase
	s    : the subsequence
    '''

    if lexical_quality(substr) <0:
	print 'DLG of {} is {}'.format(substr,-1000)
	return -1000

    corpus_len = len(corpus)
    substr_len = len(substr)


    substr_freq = occurrences(corpus,substr)
    new_corpus_len = corpus_len - substr_freq*substr_len + substr_freq + substr_len + 1
    #print s+' occurs '+ str(cs) + ' times'
    
    new_DL = calc_new_DL(unigram_freq,substr,substr_freq,new_corpus_len)
    #print substr,' ',substr_freq,' times. ' ,DL,'   ',new_DL
    #raw_input('')
    dlg = (DL - new_DL) /substr_freq
    print 'DLG of {} is {}'.format(substr,dlg)
   
    #norm_DLG = dlg*1.0/DL
    #if dlg<0 :
	#dlg = 0
    #print dlg
    return dlg  #normalised to be in the range 0 to 1


def OpSeg(corpus,unigram_freq,DL,text):
    n = len(text)
    OS = []
    DLG_stored = []
    maxDLG = 0


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
	  
	for j in range(k,-1,-1):
	    if j < k-25:
	        break
	
	    ngram = text[j:k+1]

	    #if occurrences(corpus,ngram)<2:
	    #    break
  	    if len(ngram) == 1 :		#commented to include constraint
	        dlgain = DLG_stored[j-1]
	    elif j>0:
		dlgain = DLG_stored[j-1]+ DLG(corpus,unigram_freq,DL,ngram)
	      
	    else:
		dlgain = DLG(corpus,unigram_freq,DL,ngram)
		


	    '''print DLG_stored
            print 'new DL', dlgain
            print 'DLG_stored is ',DLG_stored[k]'''
	    #print type(dlgain), type(lexgain), type(DLG_stored[k]), type(lex_stored[k])

#	    if (ALPHA*dlgain + BETA*lexgain) > (ALPHA*DLG_stored[k] + BETA*lex_stored[k]):
	    if (dlgain > DLG_stored[k]):

		if j>0:
	            OS[k][:] = []
                    OS[k] = copy.deepcopy(OS[j-1])
	            OS[k].append(ngram)
		#print 'ngram is ',ngram
  	            DLG_stored[k] = dlgain
                    print 'OS[{}] is now assigned {} with dlgain {} '.format(k,OS[k],DLG_stored[k])
 		
		elif j==0:
		    OS[k][:]=[]
		    OS[k].append(ngram)
		    DLG_stored[k] = dlgain		    
                    print 'OS[{}] is now assigned {} with dlgain {} '.format(k,OS[k],DLG_stored[k])

		raw_input('')
    return OS[n-1]


