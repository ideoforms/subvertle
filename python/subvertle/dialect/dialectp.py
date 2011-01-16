import nltk
import random
import re

class dialectp:
    def __init__(self):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        self.tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())

	def process(string):
		output = re.sub("\S+", "fuck", string)
		return output

