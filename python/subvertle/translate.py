from pipes import *

class translate():
	def __init__(self, pipelist, options = None):
		self.pipelist = pipelist
		self.pipechain = plumber(self.pipelist)

	def process(self, string):
		return self.pipechain.process(string)
