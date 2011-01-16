from dialect import *

class translate():
	def __init__(self, dialectName,options):
		if (dialectName=="expletive"):
			self.dialect = expletive()
		elif (dialectName=="language"):
			self.dialect = language(options)
		else:
			self.dialect = expletive()

	def process(self, string):
		return self.dialect.process(string)
