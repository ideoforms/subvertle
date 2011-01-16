import random
from dialectp import *

class expletive (dialectp):
	swears=[]
	alpha = 1

	def __init__(self):
		self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
		self.tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())
		makeSwear()

	def makeSwear():
		fd = open("swearwords.dat")
		for line in fd.readlines():
			swears.append(line)

	def getSwear():
		index = random.paretodistribution(alpha)*len(swears)
		return swears[index]

	def process(self, text):
		tokenized = self.tokenizer.tokenize(text)
		tagged = self.tagger.tag(tokenized)

		done = {}
		for word, type in tagged:
			if word in done:
				continue
			# # # print "%s: %s" % (type, word)
			if type and type[0] == 'N' and random.random() < 0.4:
				swear = makeSwear()
				text = re.sub(r"\b%s\b" % word, "%s %s" % swear, word, text)
				done[word] = 1

		return text


