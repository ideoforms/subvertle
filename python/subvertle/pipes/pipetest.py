#!/usr/bin/env python

from plumber import *

if __name__ == "__main__":
	print "Translating a line..."
	# use elements "cockney" "expletive" "lolspeak" anything else will be treated as a language
	# i.e. the definitions in the language.py "en" "es" "fr", though the language is a list itself
	# no checks on the functioning of that, and much more error protection needed. Just wanted
	# something that acted as a high level controller
	#chain = plumber(["expletive",["es","fr","en"]])
	chain = plumber(["expletive","lolspeak"])
	line = "Hello your eyes and face are lovely, bye"
	result = chain.process(line)
	print result

