
import sys
import os
from string import *


from pipe import *
"""Simply perform a lexigraphic swap from one word to a different (set of) word(s)

"""
class swap(pipe):

	def __init__(self,parameters={},child=None):
		pipe.__init__(self,parameters,child)
		self.lookup={}
		if not parameters.has_key('map'):
			print "Error: Need to inform swap() object of map to use"
			sys.exit(1)
		self.makeLookup(parameters['map'])

	# create the lookup table
	def makeLookup(self,map):
		filename = map+".dat"
		if not os.path.isfile(filename):
			print "Error: swap() can't find the mapping file: "+filename
		fd = open(filename) 
		for line in fd.readlines():
			relation = split(line,'\t')
			self.lookup[relation[0].lower()]=relation[1].lower().rstrip('\n')

	def transform(self,string):
		slang=[]
		boundary = re.compile(r' ')
		words = boundary.split(string)
		#print "performing transform"
		for word in words:
			newword=""
			if (self.lookup.has_key(word.lower())):
				newword=self.lookup[word.lower()]
			else:
				newword=word
			#print "doing "+word+" to "+newword
			slang.append(newword)

		rv = " ".join(slang)
		return rv

