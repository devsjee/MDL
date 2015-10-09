import plot_histogram
import create_corpus


def main():
	f_names = ['output_brown_religion.txt','output_coffee.txt']
	for fname in f_names:
		corpus = create_corpus.load_corpus(fname[7:]) #load corpus with space replaced by underscores,lowercase and all punc removed
		i_vocab = create_corpus.form_vocab(corpus) #number of unique words..	vocab is a dict
		vocab = output_vocab(fname)
		sort_vocab = plot_histogram.sort(vocab)
		err_vocab = error(i_vocab,sort_vocab)
		plot_histogram.write_vocab(err_vocab,'hist_'+fname)
		print 'Average word length is ',avg_word_length(vocab)


def error(i_vocab,vocab):
	temp = vocab[:]
	for item in vocab:
		if item[0] in i_vocab:
			temp.remove(item)

	return temp

def avg_word_length(vocab):
	total = 0
	count =0
	for word in vocab:
		total+= len(word)*vocab[word]
		count+=vocab[word]

	return total*1.0/count

def output_vocab(fname):
	f = open(fname,'r')
	output = f.readlines()
	output = str(output)
	words = output.split(' ')

	vocab = {}
	for word in words:
		if word != ' ':
			count = vocab.get(word,0)
			vocab[word] =count+1
	f.close()
	return vocab

if __name__ == '__main__':
	main()
	
