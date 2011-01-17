import random
from dialectp import *

class expletive (dialectp):
	swears=[]
	alpha = 1
	blacklist={}
	blacklist["haven't"]=1
	blacklist["don't"]=1
	blacklist["t"]=1

	def __init__(self):
		self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
		self.tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())
		self.makeSwear()

	def ignoreWord(self,word):
		if (self.blacklist.has_key(word)):
			return True
		return False

	def makeSwear(self):
		fd = open("subvertle/dialect/swearwords.dat")
		for line in fd.readlines():
			self.swears.append(line)

	def getSwear(self):
		#print "swear count: %d"%len(self.swears)
		#index = random.paretovariate(self.alpha)*(len(self.swears)-1)
		index = random.random()*len(self.swears)
		#print "swear length: %d random %d" % (len(self.swears),index)
		return self.swears[int(index)]

	def process(self, text):
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
				text = re.sub(word, r" \b%s\b%s" % (swear, word), text)
				done[word] = 1

		return text


