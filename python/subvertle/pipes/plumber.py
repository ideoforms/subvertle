from pipe import *
from swap import *
from expletive import *
from piglatin import *
from language import *
from opera import *

"""I am a plumber. I lay pipes.
"""
class plumber:

	# Give me a list of 'pipe' types or languages and I will make and link them
	# the pipes will be applied in order left to right. The language type has to 
	# be a list itself, for languages to be translated through
	def __init__(self,pipelist):
		self.pipeline = None
		for pipe in pipelist:
			print pipe
			if (pipe=="expletive"):
				self.pipeline = expletive({}, self.pipeline)
			elif (pipe=="cockney"):
				self.pipeline = swap({'map':'cockney'}, self.pipeline)
			elif (pipe=="lolspeak"):
				self.pipeline = swap({'map':'lolspeak'}, self.pipeline)
			elif (pipe=="piglatin"):
				self.pipeline = piglatin({}, self.pipeline)
			elif (pipe=="opera"):
				self.pipeline = opera({}, self.pipeline)
			#elif (pipe=="language"):
				# need something pretty clever here for efficiency
				#print "Error: Not done yet"
				#self.pipeline = language(, self.pipeline)
			else:
				self.pipeline = language({'languages':pipe}, self.pipeline)

	# pump the string through the pipeline
	def process(self,string):
		return self.pipeline.process(string)



