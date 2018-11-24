from nltk.tokenize import sent_tokenize, RegexpTokenizer
from collections import Counter
import math
import pickle

class ExtractiveSummarizer :
	def __init__(self, corpus = "cnn", scoring = 'tf-idf') :
		# with open("cnn10000.pkl", "rb") as fp :
		# 	self.corpus = pickle.load(fp)

		self.init_idf()
		self.scoring = scoring

	# TF-IDF FUNCTIONS

	def init_idf(self) :
		with open('df.pkl','rb') as fp:		
			self.idf = pickle.load(fp)

	def get_idf(self, word) :
		N = 10000
		# N = len(self.corpus[0])
		return self.idf.get(word, math.log(N, 10))

	def get_sorted_indices(self, sentences) :
		indices = list(range(len(sentences)))

		if self.scoring == 'tf-idf' :
			# term frequency - number of times a word occurs in a document.
			tf = {}
			for sentence in sentences :
				for word in sentence :
					if word == '.' or word == ',' or word == '?' or word == '"' or word == '\'' or word == '(' or word == ')' or word == '“' or word == '”' :
						continue
					tf[word] = tf.get(word, 0) + 1
			indices.sort(key = lambda i : sum([tf.get(word, 0) * self.get_idf(word) for word in sentences[i]]) / len(sentences[i]), reverse = True)

		elif self.scoring == 'bayes' :
			indices.sort(key = lambda i : sum([self.word_score.get(word, 0) for word in sentences[i]]) / len(sentences[i]), reverse = True)

		return indices

	def summarizer(self, text, sentence_count = 5) :
		# preprocess
		rem_list = ['“', '”', '"']
		for rem in rem_list :
			text = text.replace(rem, '')
		
		sentences = sent_tokenize(text)
		original_sentences = list(sentences)

		mytokenizer = RegexpTokenizer(r'\d+\.\d+|[^\W\d]+|\d+')
		sentences = [mytokenizer.tokenize(sentence) for sentence in sentences]

		sentences = [[word.lower() for word in sentence] for sentence in sentences]

		# number of sentences
		N = len(sentences)

		# sort sentence indices based on tf-idf score
		indices = list(range(N))

		indices = self.get_sorted_indices(sentences)
		indices = set(indices[:sentence_count])

		# append highest scoring sentences in order to get the summary
		summary = []
		for i in range(len(original_sentences)) :
			if i in indices :
				summary.append(original_sentences[i])
		summary = " ".join(summary)
		return summary
