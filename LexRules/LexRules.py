import string
from helpers import *

def DLG(corpus,unigram_freq,DL,substr):
    ''' calculates the gain in description length brought about by 
	a sequence s
	freq : dict containing the frequency of unigrams
	text : space removed continous corpus text in lowercase
	s    : the subsequence
    '''
    corpus_len = len(corpus)
    substr_len = len(substr)
	
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
	

    return dlg

def lexical_quality(substr):
	### added on 08-09-15 to include the constraint that a valid English word will have atleast one syllable with one nuclues
    substr_len = len(substr)
	
    flag = False
    for char in substr:
	if str.isalpha(char):
	    flag = True
	    break
	else:
	    continue

    if flag == False:
	return 0
	

    vowels = ['a','e','i','o','u']
    v_count = 0

    '''try: 
	if str.isdigit(substr) == True:
	    return -(1.0/len(substr))
	elif alpha(substr) == False:
	    return -1000

    except Exception:
	pass'''

    if substr_len == 1 and substr != 'a' and substr != 'i':
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
	
    if substr[-2:] in {'db','km','td','kd','md','bd','cd','fd','gd','hd','jd','pd','qd','sd','vd','wd','xd','yd','zd'}:
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

def read_segments(FNAME):
	data = ''
	with open(FNAME,'r') as f:
		data = f.readlines()
		data = data[0]
	
	segments = data.split('  ')
	return segments

def lexRules(FNAME):
	corpus = load_corpus("BROWN",'_') #load corpus with space replaced by underscores,lowercase and all punc removed
	vocab = form_vocab(corpus,'_') #number of unique words	vocab is a dict
	corpus = increase_DELIM(corpus,'_',0)
	freq = ngrams_freq(corpus,1)
	DL = corpusDL(corpus,freq)

	segments = read_segments(FNAME)
	output = []
	index = 0

	output.append(segments[0])
	index+=1

	for i in range(1,len(segments)-1):
		lex_qual = lexical_quality(segments[i])
		if lex_qual < 0 :
			print segments[i]
			#raw_input('')
			left = lexical_quality(output[index-1]+segments[i])
			right = lexical_quality(segments[i]+segments[i+1])
			if left>right:
				output[index-1] = output[index-1]+segments[i]
			elif right>left:
				segments[i+1] = segments[i]+segments[i+1]		
			else:
				left = DLG(corpus,freq,DL,output[index-1]+segments[i])
				right = DLG(corpus,freq,DL,segments[i]+segments[i+1])
				if left>right:
					output[index-1] = output[index-1]+segments[i]
				elif right>left:
					segments[i+1] = segments[i]+segments[i+1]		
				else:
					output.append(segments[i])
					index+=1	
		else:
			output.append(segments[i])
			index+=1
		

	with open('lex_output_'+FNAME,'w') as f:
		for seg in output:
			f.write(seg+'  ')

	rules = []
	with open('borders.txt','r') as f:
		temp = f.readline()
		while len(temp) >0:
			rules.append(temp.strip())
			temp =f.readline()
	print len(rules)
	
	output_old = output[:]
	output_new = []
	for rule in rules:
		output_new =[]
		for seg in output_old:
			index = seg.find(rule)
			if index!=-1:
				output_new.append(seg[0:index+1])
				output_new.append(seg[index+1:])
			else:
				output_new.append(seg)

		output_old = output_new[:]	
		

	with open('lex_output_final_'+FNAME,'w') as f:
			for seg in output_new:
				f.write(seg+'  ')

	return output_new


if __name__ == "__main__":
	FNAME = "out_main_BROWN"
	lexRules(FNAME)



