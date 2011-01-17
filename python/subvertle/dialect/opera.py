from gensim import corpora, models, similarities
VSM_CORPUS = 'hug.mm'
VSM_DICT = 'hug.dict'
VSM_MODEL = 'hug.lsi10'


class opera(dialect):
	"""
	does a swap and replace of the most similar line from the hansel und gretel surtitles about 1 out of 5 times
	"""
	def __init__(self):
		self.dictionary = corpora.Dictionary.load(VSM_DICT)
		self.corpus = corpora.MmCorpus(VSM_CORPUS)
		self.tfidf = models.TfidfModel(corpus)
		self.lsi_model = models.lsimodel.LsiModel.load(VSM_MODEL)
		self.index = similarities.MatrixSimilarity(self.lsi_model[self.corpus])
	def process(self, string):
		return string

