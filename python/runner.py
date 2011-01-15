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
        source = subfetch.fetch(settings.url)
        translator = subtranslate(settings.dialect)
        moodmeter = submoodmeter()
        streamer = substreamer()

        print " - processing captions (%d)" % len(source.captions)
        for caption in source.captions:
            caption.translated = translator.process(caption.text)
            caption.mood = moodmeter.process(caption.text)

        print " - starting speech generator thread"
        settings.cachedir = settings.cachedir % source.id
        generator = thread(target = generate_thread, args = (settings, captions, queue))
        generator.start()

        print " - buffering (%ds)" % settings.buffertime
        time.sleep(settings.buffertime)

        streamer.stream(source.rtspUrl)
        vocals = thread(target = vocal_thread, args = (queue,))
        vocals.start()

    # except Exception, e:
    #     print "runner.py failed: %s" % e

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

    print "      url: %s" % settings.url
    print "  dialect: %s" % settings.dialect

def generate_thread(settings, captions, queue):
    """ thread to generate speech samples """
    synth = subvocalsynth(cachedir = settings.cachedir)
    for caption in captions:
        # generate audio
        caption.audiofile = synth.generate(caption)
        queue.put(caption)

    print "*** all audio processing done ***"

def music_thread(captions):
    """ generates some music """
    pass

def vocal_thread(queue):
    """ runs through a queue of upcoming events, ordered by expected time """
    t0 = time.time()
    # probably need some try/except stuff in here
    nextEvent = queue.get()
    while True:
        now = time.time() - t0
        if now > nextEvent.start:
            # handle audio event
            print nextEvent
            nextEvent = queue.get()
            
        time.sleep(settings.clockperiod)

def usage():
    print "usage: runner.py [-d dialect] [url]"

if __name__ == "__main__":
    main(sys.argv[1:])


