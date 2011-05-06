import nltk
import random
import re

class pipe:
	def __init__(self, parameters={}, child=None):
		self.parameters = parameters # dict of paremeters
		self.child = child# child filter (apply first) or None
		self.pip = "superclass" # should be overridden to give type

	# recusively process the string, women and children first
	def process(self,string):
		if self.child is None:
			#print "No child"
			return self.transform(string) # do nothing
		#print "Using a child"
		output = self.child.process(string)
		return self.transform(output)

	# method to subclass
	def transform(string):
		return string

