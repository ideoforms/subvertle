#!/usr/bin/python

import sys
import settings
from termcolor import colored
from subvertle import *

colors = [ "red", "yellow", "green", "blue", "magenta", "cyan", "white" ]
colorhash = {}

if len(sys.argv) < 2:
	print "usage: %s <url>" % sys.argv[0]
	sys.exit()

source = fetch().fetch(sys.argv[1])
# translator = translate(settings.dialect)

for caption in source.captions:
	if caption.style in colorhash:
		color = colorhash[caption.style]
	else:
		color = colors.pop(0)
		colorhash[caption.style] = color
	
	print colored(caption.text, color)

	# caption.translated = translator.process(caption.text)
	# print colored(" - %s" % caption.translated, color)
