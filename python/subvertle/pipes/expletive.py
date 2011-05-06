import random
import os
from pipe import *

class expletive (pipe):
	swears=[]
	alpha = 1
	blacklist={}
	blacklist["haven't"]=1
	blacklist["don't"]=1
	blacklist["t"]=1

	def __init__(self, parameters = None, child = None):
		pipe.__init__(self,parameters,child)
		self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
		self.tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())
		self.makeSwear()

	def ignoreWord(self, word):
		if word in self.blacklist:
			return True
		return False

	def makeSwear(self):
		datfile = os.path.join(os.path.dirname(__file__), "swearwords.dat")
		fd = open(datfile)
		for line in fd.readlines():
			self.swears.append(line.rstrip())

	def getSwear(self):
		#print "swear count: %d"%len(self.swears)
		#index = random.paretovariate(self.alpha)*(len(self.swears)-1)
		return random.choice(self.swears)

	def transform(self, text):
		tokenized = self.tokenizer.tokenize(text)
		tagged = self.tagger.tag(tokenized)

		done = {}
		for word, type in tagged:
			if word in done:
				continue
			if self.ignoreWord(word):
				continue
			# # # print "%s: %s" % (type, word)
			if type and type[0] == 'N' and random.random() < 0.4:
				swear = self.getSwear()
				text = re.sub(r"\b%s\b" % word, "%s %s" % (swear, word), text)
				done[word] = 1

		return text


