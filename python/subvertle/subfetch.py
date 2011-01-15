#!/usr/bin/perl

# Given an iPlayer URL return subtitle list in format:
# id, start, end, text

import string
import sys
import urllib2
import re
import time
from xml.dom.minidom import parse
from subtitle import *
from media import *

class subfetch:
	urlre = re.compile('/episode/(.*?)/')
	linere = re.compile('begin="([\d:\.]+)" id="(.*)" end="([\d:\.]+)">(.*)')
	tagre = re.compile('<.*?>')
	suburlre = re.compile('"(.*?_prepared.xml)')
	vpidre = re.compile('<item kind="programme".*?identifier="(.*?)".*?>')

	def __init__(self):
		self.urlre = re.compile('/episode/(.*?)/')
		self.linere = re.compile('begin="([\d:\.]+)" id="(.*)" end="([\d:\.]+)">(.*)')
		self.brre = re.compile('<br />')
		self.tagre = re.compile('<.*?>')
		self.suburlre = re.compile('"(.*?_prepared.xml)')
		self.vpidre = re.compile('<item kind="programme".*?identifier="(.*?)".*?>')

	def programID(self,programurl):
		print "Program: "+programurl
		m = subfetch.urlre.search(programurl);
		if (m==None):
			print "Error: no URL match!"
			return None
		return m.group(1)

	def getVPID(self,id):
		url = "http://www.bbc.co.uk/iplayer/playlist/"+id
		response = urllib2.urlopen(url)
		m = self.vpidre.search(response.read())
		if (m):
			return m.group(1)
		print "Error: cant find pips :/"
		sys.exit(1)

	# pull out media descriptions
	def parseMediaSelector(self,id):
		url="http://www.bbc.co.uk/mediaselector/4/mtis/stream/"+id
		response = urllib2.urlopen(url)
		rv={}
		dom = parse(response)
		root = dom.childNodes[0];
		for node in root.childNodes:
			if node.nodeType == node.ELEMENT_NODE:
				# kind = { video, captions }
				kind = node.getAttribute("kind");
				if kind == "captions":
					connection = node.childNodes[0]
					print "subtitles: %s" % connection.getAttribute("href")
					rv['suburl']=connection.getAttribute("href")
				elif kind == "video":
					service = node.getAttribute("service")
					if service == "iplayer_streaming_n95_wifi":
						connection = node.childNodes[0]
						print "video: %s" % connection.getAttribute("href")
						rv['urlurl'] = connection.getAttribute("href")
		return rv

	def XMLtoCaptions(self,xml):
		lines = string.split(xml,"</p>")
		rv = []
		for line in lines:
			m = self.linere.search(line)
			if (m==None):
				continue
			else:
				# id, start, end, TXT
				text = m.group(4)
				text = self.brre.sub(' ', text)
				cleantxt = self.tagre.sub('', text)
				sub = subtitle(m.group(2),self.toSeconds(m.group(1)),self.toSeconds(m.group(3)),cleantxt)
				#print cleanl
				#rv.append(cleanl)
				rv.append(sub)
		return rv

	def toSeconds(self,timestr):
		hour = int(timestr[0:2])
		min = int(timestr[3:5])
		sec = int(timestr[6:8])
		return str(hour*3600 + min*60 + sec) + timestr[8:11]

	# traverse the url indirection
	def getRTSPURL(self,urlurl):
		response = urllib2.urlopen(urlurl)
		return response.read()

	def getSubs(self,url):
		response = urllib2.urlopen(url)
		return response.read()

	def fetch(self,url):
		# begin the long road of boring translation
		id = self.programID(url)
		print "Program ID: "+id
		m = media(id)
		m.vpid = self.getVPID(m.id)
		print "VPID: "+m.vpid
		# get details of this programme
		m.mediaDetails = self.parseMediaSelector(m.vpid)
		print "RTSP URL URL: "+ m.mediaDetails['urlurl']
		m.rtspUrl = self.getRTSPURL(m.mediaDetails['urlurl'])
		print "RTSP: "+m.rtspUrl
		# get the subtitles
		m.subs = self.getSubs(m.mediaDetails['suburl'])
		# parse subtitle XML
		m.captions = self.XMLtoCaptions(m.subs)
		return m


###########
# Main body
###########
if __name__ == "__main__":
	# Get iplayer URL from command line
	if (len(sys.argv) != 2):
		print "Error: Need program ID...\nUsage: subfetch.py <URL>"
		sys.exit(1)
	programurl = sys.argv[1]


	# output sutitles
	for line in lines:
		print line
		sys.exit(1)


