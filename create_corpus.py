import mainDLG

base_low = 0
base_mid = 0
base_high = 0

mean = 10

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

f_names =['stories.txt']

def contribution(vocab):
	size = 0
	for item in vocab:
		size+= len(item[0])*item[1]
	return size

def load_corpus(fname):
	''' takes the filename in which space separated text is located 
	and returns as the continous text in lowercase,punctuations removed and spaces replaced by underscores
        fname : file name as string
	'''
	data = ''
	punctuation ='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
	with open(fname,'r') as f:
		for line in f:
			text = line.lower()
	    		for punc in punctuation:
				text = text.replace(punc,' ')
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

	global base_low
	global base_mid
	global base_high
	global mean

	vocab ={}
	words = corpus.split('_')
	for word in words:
		count = vocab.get(word,0) + 1
		vocab[word] = count

	for word in vocab:
		freq = vocab[word]
		if freq == 1:
			base_low+=1
		elif freq <mean:
			base_mid+= freq
		else:
			base_high+= freq

        return vocab
	
	
def form_boundaries(corpus):
	'''takes the '_' separated text and forms a set with start position and length
	of segment as an element
	'''
	boundaries = set()
	index = 0
	words = corpus.split('_')
	for word in words:
		length = len(word)
		boundaries.add((index,length))
		index+=length

	return boundaries
		
def calc_precision(vocab,output,boundaries):
	''' output : list format
	if a segment is present in boundaries,it is counted as correct.
	to check if its present, we form an element with starting position and 
	length of segment as a tuple
	'''
	correct = 0
	index = 0

	low_correct = 0
	mid_correct = 0
	high_correct = 0
	
	global mean,base_low,base_mid,base_high	

	for word in output:
		length = len(word)
		key =(index,length)
		if key in boundaries:
			correct+=1
			freq = vocab.get(word,0)
			if freq ==0 :
				print 'zero freq word ',word
				continue
			if freq == 1:
				low_correct+=1
			elif freq < mean:
				mid_correct+=1
			else:
				high_correct+=1
		index+=length
	print 'precision wrt word boundaries is '+str(correct*1.0/len(output))
	print '\t freq 1 precision : ',str(low_correct*1.0/base_low)
	print '\t freq mid precision : ',str(mid_correct*1.0/base_mid)
	print '\t freq high precision : ',str(high_correct*1.0/base_high)
	print 'Recall wrt boundaries is ' + str(correct*1.0/len(boundaries))	

def space_strip(corpus):
	''' takes the corpus and removes all occurrences of '_' and returns it
	corpus : continous text (string)
	'''
	corpus = corpus.replace('_','')
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
	#f_names =['temp.txt','coffee.txt','brown_religion.txt']
	f_names =['coffee.txt','editorial.txt','news_brown.txt', 'webtext_nltk.txt','alice.txt','brown_religion.txt']


	for fname in f_names:
		corpus = load_corpus(fname) #load corpus with space replaced by underscores,lowercase and all punc removed
		vocab = form_vocab(corpus[0:100000]) #number of unique words	vocab is a dict
		word_boundaries = form_boundaries(corpus[0:100000])
		corpus = space_strip(corpus[0:100000]) #corpus size in number of chars after removing space
	
		#sort_vocab = sort(vocab)	#sorted vocab in the form a list of elements [(key,freq),..]
		#freq_vocab1 = trim(sort_vocab,1)
		#freq_vocab10 = trim(sort_vocab,10)
		#freq_vocab50 = trim(sort_vocab,50)
		#freq_vocab100 = trim(sort_vocab,100)

		print fname  + " corpus size : "+str(len(corpus))
		#print 'vocab size ' + str(len(vocab.keys()))
		#print "contribution of freq vocab in corpus size : "+ str(contribution(freq_vocab))

		#print vocab	
		freq = mainDLG.ngrams_freq(corpus,1)
	        DL = mainDLG.corpusDL(corpus,freq)
		output= mainDLG.OpSeg(corpus,freq,DL,corpus)
		with open('output_'+fname,'w') as f:
			for word in output:
				f.write(word+ '  ')
	
		calc_precision(vocab,output,word_boundaries)
		mainDLG.calc_precision(vocab,output)
		#post_output = pre_calc_recall(output)	      
		#calc_recall(post_output,vocab,0)	#vocab is a dict, freq_vocab is a list
		#calc_recall(post_output,freq_vocab1,1)	
		#calc_recall(post_output,freq_vocab10,10)	
		#calc_recall(post_output,freq_vocab50,50)	
		#calc_recall(post_output,freq_vocab100,100)	
		print

if __name__ == '__main__':
	main()
