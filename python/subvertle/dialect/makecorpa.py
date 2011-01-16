"""
process some text lines into a gensim corpus and dictionary
usage: makecorpa.py infile outcorpa outdict

"""


import sys

from gensim import corpora, models, similarities

stoplist = set(''.split())# basic stop list: 'for a of the and to in'

iH = open(sys.argv[1])
oH = open(sys.argv[2], 'w')
oDH = open(sys.argv[3], 'w')
oH.close()
oDH.close()

print 'tokenizing...'

documents = iH.readlines()
texts = [[word for word in document.lower().split() if word not in stoplist]
			for document in documents]
allTokens = sum(texts, [])
tokensOnce = set(word for word in set(allTokens) if allTokens.count(word) == 1)
texts = [[word for word in text if word not in tokensOnce]
			for text in texts]

print "creating dictionary..."
dictionary = corpora.Dictionary(texts)
dictionary.save(sys.argv[3])

print "creating corpus..."
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.saveCorpus(sys.argv[2], corpus) # store to disk, for later use

