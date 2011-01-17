#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Benjamin Fields on 2011-01-15.
Copyright (c) 2011 Goldsmith University of London. All rights reserved.
"""

import sys
import os
import urllib,urllib2
import unittest
import canoris
import math
from simplejson import loads, dumps
from my_key import API_KEY



canoris.Canoris.set_api_key(API_KEY)
DEFAULT_MELODY = [(30, 60, 100),
					(30, 62, 100),
					(30, 64, 100),
					(30, 67, 100),
					(30, 69, 100)]

class melodypopper(object):
	def __init__(self, melody = []):
		self.current = 0
		self.melody = melody
	def __iter__(self):
		return self
	def __len__(self):
		return len(self.melody)
	def next(self):
		if (self.current == len(self.melody)-1):
			self.current = 0
			return self.melody[len(self.melody) - 1]
		self.current += 1
		return self.melody[self.current - 1]
			
			

class singSomeText():
	"""
	class is used to define and produce synthetic song from text
	"""
	def __init__(self, lang='english',voice='lara', ticklength=0.01, breaklength=10, melody=melodypopper(DEFAULT_MELODY), transform=None):
		"""
		setup the instance with the following fields:
			lang (for text to phoneme translation) - a string known by http://docs.canoris.com/reference.html#resources-language
			voice (for song synth) - a string known by http://docs.canoris.com/operation_vocaloid.html
			ticklength - foat minimum unit for duration, in seconds
			breaklength - num of ticks to break between words, double between sentences
			melody (for song synth) - a melodyPopper class wrapped around a list of tuples of the form (duration, pitch, velocity) duration is in ticklength
		"""
		self.lang=lang
		self.voice=voice
		self.ticklength=ticklength
		self.melody=melody
		self.breaklength = breaklength
		self.transform=transform
		
	def pingTemplate(self, templateName):
		"""
		creates a template named templateName with the current fields 
			(except melody, which is always set on run)
		trys a POST first, if that doesn't work attemps a PUT which will update an existing entry
		though updates don't really work, try to delete templates when done with then.
		"""
		template = [{"operation":"vocaloid",
			"parameters":{"voice":str(self.voice),"sequence":"{{ substitute_this }}"}}]
		if self.transform != None:
			template.append({"operation":"voice_transform", 
			"parameters":{"preset":str(self.transform)}})
		try:
			return canoris.Template.create_template(templateName, template)
		except urllib2.HTTPError:
			template_ob = canoris.Template.get_template(templateName)
			template_ob['template'] = template
			template_ob.update()
			return template_ob
	
	def singThisText(self,some_text, templateName, tieWord=True):
		"""
		sends some_text to the Text2Phoneme process, then iterates through the melody sequence to build the synthesis task. Pushes the whole thing through a template templateName, which should align with current properties. Then submit the task, return the task object on sucess.
		
		if tieWord = False, multisylabic words can change pitch mid word. 
			By default, 
		"""
		phoneme_pieces = canoris.Text2Phonemes.translate(some_text, self.voice, self.lang)
		xmlString = """<melody ticklength='%f'>"""%self.ticklength
		current_melody_idx = 0
		for word in phoneme_pieces['phonemes']:
			joinedPhonemes = ''
			for idx, syl in enumerate(word):
				if idx == 0 or not tieWord:
					noteTuple = self.melody.next()
				joinedPhonemes = syl[0]
				for pho in syl[1:]:
					joinedPhonemes += " %s"%pho
				xmlString += """<note duration='%i' pitch='%i' velocity='%i' phonemes='%s'/>"""%\
					(int(math.log(len(syl)+1)*noteTuple[0]),noteTuple[1],noteTuple[2],joinedPhonemes)
			xmlString += """<rest duration='%i'/>"""%self.breaklength
		xmlString += "</melody>"
		print "synthesizing vocals..."
		task_ob = canoris.Task.create_task(templateName,{'substitute_this':xmlString})
		return task_ob
		
	def isAudioAvailable(self,task_ob):
		"""
		checks to see if the task associated with task_ob is done.  If it is return the uri for the completed resource.  If it's not return None.
		"""
		task_ob.update()
		if task_ob['complete']:
			return True
		return False
		
	def grabAudio(self, task_ob, file_name):
		"""
		download audio from task_ob.  Assumes it's available, will fall over if not.  Saves wavefile to file_name, which should alread have the appropriate extension.
		"""
		print "dl'ing "+task_ob['output']+"/serve?api_key="+API_KEY
		req = urllib2.urlopen(task_ob['output']+"/serve?api_key="+API_KEY)
		CHUNK = 16 * 1024
		fp = open(file_name, 'wb')
		while True:
			chunk = req.read(CHUNK)
			if not chunk: break
			fp.write(chunk)
	
	


class untitledTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()
