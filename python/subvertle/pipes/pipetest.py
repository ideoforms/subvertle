#!/usr/bin/env python

from plumber import *

if __name__ == "__main__":
	print "Translate a line"
	chain = plumber([["es","fr","en"]])
	line = "Hello your eyes and face are lovely bye"
	result = chain.process(line)
	print result

