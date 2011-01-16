#!/usr/bin/python

import sys
sys.path.append("..")

import time
import werkzeug
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, jsonify, make_response
from subvertle import *

app = Flask(__name__)

@app.route('/get', methods = ['GET', 'POST'])
def get():
	""" get subtitles for a given URL """
	print "getting url"
	url = request.args.get('url')
	print "url: %s" % url
	source = fetch().fetch(url)

	captionlist = []
	for caption in source.captions:
		captionlist.append({
			"text"  : caption.text,
			"start" : caption.start,
			"end"   : caption.end
		})
	# print "list: %s" % captionlist
	# return jsonify(captions = captionlist)
	# return jsonify(result = captionlist)
	return jsonify(result = captionlist)

@app.route('/_add')
def add():
	return render_template('add.html')

@app.route('/_add_numbers')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	print "returning with %d, %d" % (a, b)
	return jsonify(result=a + b)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)
