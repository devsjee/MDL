import create_corpus

def sort(vocab):
	vocab_list =[]
<<<<<<< HEAD
	total = 0
	for key in vocab:
		vocab_list.append((key,vocab[key]))
		total+=vocab[key]
	vocab_list.sort(key= lambda x:x[1],reverse =True)

	print 'maximum is ',vocab_list[0][1]
	print 'minimum is ',vocab_list[-1][1]
	print 'average is ',(total*1.0)/len(vocab)
	print 'returning sorted vocab list..'

=======
	for key in vocab:
		vocab_list.append((key,vocab[key]))
	vocab_list.sort(key= lambda x:x[1],reverse =True)
	
	print 'returning sorted vocab list..'
>>>>>>> ba02c4f692249cdf8bcbc2930b4c74b2499e2e75
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

#f_names = ['coffee.txt','brown_religion.txt']

<<<<<<< HEAD
f_names =['coffee.txt','editorial.txt','news_brown.txt', 'webtext_nltk.txt','alice.txt','brown_religion.txt']
=======
f_names =['coffee.txt','editorial.txt','news_brown.txt', 'webtext_nltk.txt','stories.txt','macbeth.txt','alice.txt','brown_religion.txt']
>>>>>>> ba02c4f692249cdf8bcbc2930b4c74b2499e2e75

def contribution(vocab):
	size = 0
	for item in vocab:
		size+= len(item[0])*item[1]
	return size

<<<<<<< HEAD
def main():
	for fname in f_names:
		corpus = create_corpus.load_corpus(fname) #load corpus with space replaced by underscores,lowercase and all punc removed
		vocab = create_corpus.form_vocab(corpus[0:100000]) #number of unique words..	vocab is a dict
		corpus = create_corpus.space_strip(corpus[0:100000])
		sort_vocab = sort(vocab)	#sorted vocab in the form a list of elements [(key,freq),..]
		#freq_vocab = trim(sort_vocab,1)
		#write_vocab(freq_vocab,'freq_hist_1_'+fname)
		write_vocab(sort_vocab,'hist_'+fname)
		print fname+" vocab size : "+ str(len(vocab))+ " corpus size : "+str(len(corpus))
		#print "contribution of freq vocab in corpus size : "+ str(contribution(freq_vocab))

if __name__ ==  "__main__":
	main()	
=======
for fname in f_names:
	corpus = create_corpus.load_corpus(fname) #load corpus with space replaced by underscores,lowercase and all punc removed
	vocab = create_corpus.form_vocab(corpus) #number of unique words..	vocab is a dict
	corpus = create_corpus.space_strip(corpus)
	sort_vocab = sort(vocab)	#sorted vocab in the form a list of elements [(key,freq),..]
	freq_vocab = trim(sort_vocab,1)
	write_vocab(freq_vocab,'freq_hist_1_'+fname)
	write_vocab(sort_vocab,'hist_'+fname)
	print fname+" vocab size : "+ str(len(vocab))+" freq_vocab : "+ str(len(freq_vocab)) + " corpus size : "+str(len(corpus))
	print "contribution of freq vocab in corpus size : "+ str(contribution(freq_vocab))

	
>>>>>>> ba02c4f692249cdf8bcbc2930b4c74b2499e2e75
