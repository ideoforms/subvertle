#!/usr/bin/perl

import string
import sys
import urllib2
import re
import time
from xml.dom.minidom import parse, parseString

class fetch:
	def __init__(self):
		""" some regexps needed for later parsing """
		self.urlre = re.compile('/episode/(.*?)/')
		self.vpidre = re.compile('<item kind="programme".*?identifier="(.*?)".*?>')

	def getWebData(self, url):
		""" may be able to do this with socks proxy: http://stackoverflow.com/questions/2879183/problem-with-urllib """
		response = urllib2.urlopen(url)
		return response.read()

	def getProgramID(self, programurl):
		print "Program: " + programurl
		m = self.urlre.search(programurl);
		if m == None:
			raise ValueError, "Couldn't extract program ID from URL: %s" % programurl
			return None
		return m.group(1)

	def getVPID(self,id):
		url = "http://www.bbc.co.uk/iplayer/playlist/%s " % id
		content = self.getWebData(url)
		print "content: %s" % content
		m = self.vpidre.search(content)
		if (m):
			return m.group(1)
		else:
			raise ValueError, "Couldn't extract PIP value from URL: %s" % url

	def parseMediaSelector(self,id):
		""" pull out available media descriptions """
		url = "http://www.bbc.co.uk/mediaselector/4/mtis/stream/%s" % id
		print "getting: %s" % url
		content = self.getWebData(url)
		print "got content: %s" % content
		rv = {}
		dom = parseString(content)
		root = dom.childNodes[0];

		for node in root.childNodes:
			print "node %s" % node
			if node.nodeType == node.ELEMENT_NODE:
				# kind = { video, captions }
				kind = node.getAttribute("kind")
				if kind == "captions":
					connection = node.childNodes[0]
					print "subtitles: %s" % connection.getAttribute("href")
					rv['suburl'] = connection.getAttribute("href")
				elif kind == "video":
					service = node.getAttribute("service")
					if service == "iplayer_streaming_n95_wifi":
						connection = node.childNodes[0]
						print "video: %s" % connection.getAttribute("href")
						rv['ramurl'] = connection.getAttribute("href")
		return rv

	def parseCaptions(self, xml):
		""" parse caption XML (TT) into a list of subtitle objects """
		rv = []
		styles = []
		dom = parseString(xml)
		captions = dom.getElementsByTagName("p")
		for node in captions:
			id = node.getAttribute("id");
			begin = node.getAttribute("begin");
			end = node.getAttribute("end");
			style = node.getAttribute("style");
			if not style:
				style = ""

			if style in styles:
				style = styles.index(style)
			else:
				styles.append(style)
				style = len(styles)

			text = ""
			for content in node.childNodes:
				if content.nodeType == node.TEXT_NODE:
					# print content.nodeValue
					text = text + content.nodeValue
				elif content.tagName == "br":
					text = text + " "
				elif len(content.childNodes) > 0:
					text = text + content.childNodes[0].nodeValue
			sub = subtitle(id, self.toSeconds(begin), self.toSeconds(end), style, text)
			# print "%s: %s, %s, %s, %s" % (id, begin, end, style, text)
			rv.append(sub)
		return rv

	def toSeconds(self, timestr):
		""" turn a Timed Text time string into a floating point value in seconds """
		m = re.search(r'^(\d+):(\d+):(\d+)\.(\d+)', timestr)
		if m:
			hour = int(m.group(1))
			min = int(m.group(2))
			sec = int(m.group(3))
			ms = int(m.group(4))
			return hour * 3600 + min * 60 + sec + ms / 1000.0
		else:
			raise ValueError, "Could not parse TT time value: %s" % timestr

	def getRTSPURL(self, ramurl):
		""" given the URL of a RAM file, returns the first stream (ie, first line of file) """
		response = urllib2.urlopen(url)
		return response.read()

	def getSubtitles(self,url):
		""" fetch subtitle XML file """
		response = urllib2.urlopen(url)
		return response.read()

	def fetch(self,url, manual = False):
		""" begin the long boring road of subtitle extraction """

		#-----------------------------------------------------------------------
		# 1. extract programme ID from its URL
		#-----------------------------------------------------------------------
		id = self.getProgramID(url)
		print "Program ID: " + id

		#-----------------------------------------------------------------------
		# 2. download playlist XML, and extract programme version ID 
		#-----------------------------------------------------------------------
		m = mediaSource(id)
		m.vpid = self.getVPID(m.id)
		print "VPID: " + m.vpid

		#-----------------------------------------------------------------------
		# 3. download mediaselector XML for stream source details
		#-----------------------------------------------------------------------
		m.mediaDetails = self.parseMediaSelector(m.vpid)

		#-----------------------------------------------------------------------
		# 4. extract URL of RTSP stream (if available)
		#-----------------------------------------------------------------------
		if 'ramurl' in m.mediaDetails:
			print "RAM URL: "+ m.mediaDetails['ramurl']
			m.rtspUrl = self.getWebData(m.mediaDetails['ramurl'])
			print "RTSP URL: "+m.rtspUrl
		else:
			print "no RTSP URL found :-("

		#-----------------------------------------------------------------------
		# 5. download and parse captions
		#-----------------------------------------------------------------------
		m.subtitleXML = self.getWebData(m.mediaDetails['suburl'])
		m.captions = self.parseCaptions(m.subtitleXML)
		print "got captions: %s" % m.captions

		return m


class mediaSource:
	""" simple data storage class, representing a multi-format media source """
	id = -1
	name = "Media item"
	captions = () 
	rtspUrl = ""

	def __init__(self,id):
		self.id = id

class subtitle:
	""" simple data storage class, representing single subtitle line with timing info """
	id = -1
	start = -1.0
	end = -1.0
	text = -1
	style = ""
	
	def __init__(self, id, start, end, style, text):
		self.id = id
		self.start = start
		self.end = end
		self.style = style
		self.text = text
		self.translated = ""
		self.mood = ""
		self.audiofile = None

if __name__ == "__main__":
	""" Get iPlayer URL from command line """
	if (len(sys.argv) != 2):
		print "Error: Need program ID...\nUsage: subfetch.py <URL>"
		sys.exit(1)
	programurl = sys.argv[1]

	# output sutitles
	for line in lines:
		print line
		sys.exit(1)

