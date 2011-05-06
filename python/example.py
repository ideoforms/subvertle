#!/usr/bin/python


""" Short example which fetches subtitles from a given BBC iPlayer URL,
    translates them into expletives, and outputs.

	If you're getting dependency errors and only want to access subtitles
    (without translation etc), use "from subvertle import iplayerlib" """

import sys
import settings
from subvertle import *

if len(sys.argv) < 2:
	print "usage: %s <iplayer_programme_url>" % sys.argv[0]
	sys.exit()

source = iplayerlib.fetch(sys.argv[1])
dialect = translate("expletive")
translator = translate(settings.dialect)

for caption in source.captions:
	print caption.text

	caption.translated = translator.process(caption.text)
	print " - %s" % caption.translated
