#!/usr/bin/python

# extract subtitle URL and video streaming RTSP URL from
# mediaselector XML

from xml.dom.minidom import parse

dom = parse("mediaselector-b00xjyg1.xml");
root = dom.childNodes[0];
for node in root.childNodes:
    if node.nodeType == node.ELEMENT_NODE:
        # kind = { video, captions }
        kind = node.getAttribute("kind");
        if kind == "captions":
            connection = node.childNodes[0]
            print "subtitles: %s" % connection.getAttribute("href")
        elif kind == "video":
            service = node.getAttribute("service")
            if service == "iplayer_streaming_n95_wifi":
                connection = node.childNodes[0]
                print "video: %s" % connection.getAttribute("href")
