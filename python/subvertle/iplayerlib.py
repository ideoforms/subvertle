#!/usr/bin/env python

import string
import sys
import urllib2
import re
import time
from xml.dom.minidom import parse, parseString

class IPlayerError(Exception):
    """Base class for iPlayer exceptions. """
    pass

class iplayerlib:
	""" iplayerlib: A library to access BBC iPlayer metadata, primarily
	    subtitle content.

	    Due to the DRM-protected [blech] nature of the video streams, it's sadly
	    difficult to do anything useful with these. This is left as an exercise
	    for the reader. However, it's straightforward to obtain and manipulate
	    the subtitle feeds accompanying many programmes. See the pydocs for
	    iplayerlib.fetch for details."""

	error = IPlayerError
	debug = False

	""" some regexps needed for later parsing """
	urlre = re.compile('/episode/(.*?)/')
	vpidre = re.compile('<item kind="programme".*?identifier="(.*?)".*?>')

	@classmethod
	def getProgramID(self, programurl):
		if self.debug:
			print "Program: %s" % programurl
		m = self.urlre.search(programurl);
		if m == None:
			raise ValueError, "Couldn't extract program ID from URL: %s" % programurl
			return None
		return m.group(1)

	@classmethod
	def getWebData(self, url):
		response = urllib2.urlopen(url)
		return response.read()

	@classmethod
	def getVPID(self, id):
		url = "http://www.bbc.co.uk/iplayer/playlist/%s " % id
		if self.debug:
			print "Playlist URL: %s" % url

		response = urllib2.urlopen(url)
		m = self.vpidre.search(response.read())
		if (m):
			return m.group(1)
		else:
			raise ValueError, "Couldn't extract PIP value from URL: %s" % url

	@classmethod
	def parseMediaSelector(self, id):
		""" pull out available media descriptions """
		url = "http://www.bbc.co.uk/mediaselector/4/mtis/stream/%s" % id
		if self.debug:
			print "Media selector: %s" % url
		response = urllib2.urlopen(url)
		rv = {}
		dom = parseString(response.read())
		root = dom.childNodes[0];

		for node in root.childNodes:
			if node.nodeType == node.ELEMENT_NODE:
				# kind = { video, captions }
				kind = node.getAttribute("kind")
				if kind == "captions":
					connection = node.childNodes[0]
					if self.debug:
						print " - Subtitles URL: %s" % connection.getAttribute("href")
					rv['suburl']=connection.getAttribute("href")
				elif kind == "video":
					service = node.getAttribute("service")
					if service == "iplayer_streaming_n95_wifi":
						connection = node.childNodes[0]
						if self.debug:
							print " - Video URL: %s" % connection.getAttribute("href")
						rv['ramurl'] = connection.getAttribute("href")
		return rv

	@classmethod
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

	@classmethod
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

	@classmethod
	def getRTSPURL(self, ramurl):
		""" given the URL of a RAM file, returns the first stream (ie, first line of file) """
		response = urllib2.urlopen(url)
		return response.read()

	@classmethod
	def getSubtitles(self, url):
		""" fetch subtitle XML file """
		response = urllib2.urlopen(url)
		return response.read()

	@classmethod
	def fetch(self, url, debug = None):
		""" Fetch details of an iPlayer stream based on its full URL:
		    Returns a mediaSource object, or raises a iplayerlib.error exception.

		       m = iplayerlib.fetch("http://www.bbc.co.uk/iplayer/episode/b00rrd81/Human_Planet_Oceans_Into_the_Blue/")
		       captions = m.captions
		       for caption in captions:
		           print caption.text
		"""

		if debug is not None:
			self.debug = debug

		#-----------------------------------------------------------------------
		# 1. extract programme ID from its URL
		#-----------------------------------------------------------------------
		id = self.getProgramID(url)
		if self.debug:
			print "Program ID: " + id

		#-----------------------------------------------------------------------
		# 2. download playlist XML, and extract programme version ID 
		#-----------------------------------------------------------------------
		m = mediaSource(id)
		m.vpid = self.getVPID(m.id)
		if self.debug:
			print "VPID: " + m.vpid

		#-----------------------------------------------------------------------
		# 3. download mediaselector XML for stream source details
		#-----------------------------------------------------------------------
		m.mediaDetails = self.parseMediaSelector(m.vpid)

		#-----------------------------------------------------------------------
		# 4. extract URL of RTSP stream (if available)
		#-----------------------------------------------------------------------
		if 'ramurl' in m.mediaDetails:
			if self.debug:
				print "RAM URL: "+ m.mediaDetails['ramurl']
			try:
				m.rtspUrl = self.getRTSPURL(m.mediaDetails['ramurl'])
			except Exception:
				if self.debug:
					print "Couldn't find RTSP URL."
		else:
			print "no RTSP URL found :-("

		#-----------------------------------------------------------------------
		# 5. download and parse captions
		#-----------------------------------------------------------------------
		m.subtitleXML = self.getWebData(m.mediaDetails['suburl'])
		m.captions = self.parseCaptions(m.subtitleXML)

		return m


class mediaSource:
	""" Simple data storage class, representing a multi-format media source.
	    To access the captions of a media source, use m.captions. """
	id           = -1
	vpid         = None
	name         = "Media item"
	mediaDetails = None
	subtitleXML  = None
	rtspUrl      = None

	captions = []

	def __init__(self, id):
		self.id = id

class subtitle:
	""" Simple data storage class, representing single subtitle line with timing info """
	id     = -1
	start  = 0.0
	end    = 0.0
	text   = ""
	style  = ""
	
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
	""" Get iPlayer subtitles based on specified URL. """
	if (len(sys.argv) != 2):
		print "Usage: python %s <iplayer_programme_url>" % sys.argv[0]
		sys.exit(1)

	url = sys.argv[1]

	try:
		source = iplayerlib.fetch(url, debug = False)

		captions = source.captions
		print "Found %d subtitles" % len(captions)
		for line in captions:
			print "(%s) %s" % (line.start, line.text)

	except Exception, e:
		print "fetch failed: %s" % e


