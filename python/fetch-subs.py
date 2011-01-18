#!/usr/bin/python

import sys
import settings
from subvertle import *


if len(sys.argv) < 2:
	print "usage: %s <url>" % sys.argv[0]
	sys.exit()

source = fetch().fetch(sys.argv[1])
# dialect = translate("language",["en","es"])
# translator = translate(settings.dialect)

for caption in source.captions:
	print caption.text

	# caption.translated = translator.process(caption.text)
	# print colored(" - %s" % caption.translated, color)
