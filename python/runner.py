#!/usr/bin/python

"""----------------------------------------------------------------
   SUBVERTLE!
   algorithmic processing of BBC iPlayer subtitles.
-------------------------------------------------------------------"""

import os
import sys
import getopt
import settings
from threading import Thread as thread
from Queue import Queue
from subvertle import *

def main(args):
	""" subvertle: the master operations block """
		
	init_settings(args)
	queue = Queue()

	# try:
	if True:
		# source is our media source.  
		# should contain captions and an RTSP video URL.
		#  - source.captions: list of caption events
		#  - source.rtspUrl:  string URL of RTSP stream
		print " - fetching feed information"
		source = fetch().fetch(settings.url)
		translator = translate(settings.dialect)
		mood = moodmeter()
		stream = streamer()

		print " - processing captions (%d)" % len(source.captions)
		for caption in source.captions:
			caption.translated = translator.process(caption.text)
			# print caption.text
			# print " -> %s" % caption.translated
			# caption.mood = mood.process(caption.text)

		print " - starting speech generator thread"
		settings.cachedir = settings.cachedir % source.id
		generator = thread(target = generate_thread, args = (settings, captions, queue))
		generator.start()

		print " - buffering (%ds)" % settings.buffertime
		time.sleep(settings.buffertime)

		sayqueue = Queue()
		sayer = thread(target = sayer_thread, args = (sayqueue,))
		sayer.start()

		# streamer.stream(source.rtspUrl)
		for caption in source.captions:
			queue.put(caption)
		vocals = thread(target = vocal_thread, args = (queue,sayqueue))
		vocals.start()

	# except Exception, e:
	#	 print "runner.py failed: %s" % e

def init_settings(args):
	""" load command-line settings into the global settings """
	try:
		opts, args = getopt.getopt(args, "d:")
		for o, a in opts:
			if o == "-d":
				settings.dialect = a
		if len(args) > 0:
			settings.url = args[0]

	except:
		usage()
		sys.exit(1)

	print "	     url: %s" % settings.url
	print "  dialect: %s" % settings.dialect

def generate_thread(settings, captions, queue):
	""" thread to generate speech samples """
	synth = vocalsynth(cachedir = settings.cachedir)
	for caption in captions:
		# generate audio
		caption.audiofile = synth.generate(caption)
		queue.put(caption)

	print "*** all audio processing done ***"

def music_thread(captions):
	""" generates some music """
	pass

def sayer_thread(queue):
	voices = [ "Fred", "Vicki", "Victoria", "Bruce", "Junior", "Agnes" ]
	while True:
		caption = queue.get()
		os.system('say -v %s "%s" 2>/dev/null' % (voices[caption.style], caption.translated))

def vocal_thread(queue, sayqueue):
	""" runs through a queue of upcoming events, ordered by expected time """
	t0 = time.time()
	# probably need some try/except stuff in here
	nextEvent = queue.get()
	while True:
		now = time.time() - t0
		# print "now %f, next %d\n" % (now, nextEvent.start)
		if now > nextEvent.start:
			# handle audio event
			print nextEvent.translated
			sayqueue.put(nextEvent)
			nextEvent = queue.get()
			
		time.sleep(settings.clockperiod)

def usage():
	print "usage: runner.py [-d dialect] [url]"

if __name__ == "__main__":
	main(sys.argv[1:])


