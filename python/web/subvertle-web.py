#!/usr/bin/python

import sys
sys.path.append("..")
sys.path.append(".")

import os
import time
import werkzeug
from threading import Thread as thread

from Queue import Queue
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, jsonify, make_response
from subvertle import *

app = Flask(__name__)

translator = translate("expletive", [])
captions = []

queue = Queue()

def sayer_thread(queue):
	voices = [ "Fred", "Vicki", "Victoria", "Bruce", "Junior", "Agnes" ]
	print "RUNNING SAYER"
	while True:
		caption = queue.get()
		print "saying: %s" % caption.text
		# os.system('say -v %s "%s" 2>/dev/null' % (voices[caption.style], caption.text))
		os.system('say "%s" 2>/dev/null' % caption.text)

def vocal_thread(queue, sayqueue):
	""" runs through a queue of upcoming events, ordered by expected time """
	t0 = time.time()
	# probably need some try/except stuff in here
	nextEvent = queue.get()
	while True:
		now = time.time() - t0
		# print "now %f, next %d" % (now, nextEvent.start)
		if now > nextEvent.start:
			# handle audio event
			print "putting: %s, %s" % (nextEvent.text, nextEvent.translated)
			#snd = swmixer.Sound(nextEvent.audiofile)
			#snd.play()

			sayqueue.put(nextEvent)
			nextEvent = queue.get()
			
		time.sleep(0.01)



@app.route('/get', methods = ['GET', 'POST'])
def get():
	""" get subtitles for a given URL """
	print "getting url"
	url = request.args.get('url')
	dialect = request.args.get('dialect')
	print "url: %s, dialect: %s" % (url, dialect)
	manual = (dialect == "spanish")
	source = fetch().fetch(url, manual)

	global captions
	captions = []
	captionlist = []
	for caption in source.captions:
		if dialect == "expletive":
			caption.text = translator.process(caption.text)
			
		captionlist.append({
			"text"  : caption.text,
			"start" : caption.start,
			"end"   : caption.end
		})

		captions.append(caption)

	return jsonify(result = captionlist)


@app.route('/start')
def start():
	print "starting say thread"
	sayqueue = Queue()
	sayer = thread(target = sayer_thread, args = (sayqueue,))
	sayer.start()
	
	# print "got captions: %s" % captions
	for caption in captions:
		queue.put(caption)

	vocals = thread(target = vocal_thread, args = (queue,sayqueue))
	vocals.start()
	return "hello"

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = False)

