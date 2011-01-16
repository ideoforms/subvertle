from singSomeText import *
import os.path as path

import time

class vocalsynth(object):
	def __init__(self, cachedir = './'):
		self.cachedir = cachedir
		self.sst = singSomeText()
		
	def generate(self, caption):
		filename = path.join(self.cachedir,caption.id +'.wav')

		# got precached version of this speech
		if os.path.exists(filename):
			return filename

		if caption.style%5 == 0:
			self.out = self.sst.singThisText(caption.translated, 'vox')
		elif caption.style%5 == 1:
			self.out = self.sst.singThisText(caption.translated, 'voxM1')
		elif caption.style%5 == 2:
			self.out = self.sst.singThisText(caption.translated, 'voxF2')
		elif caption.style%5 == 3:
			self.out = self.sst.singThisText(caption.translated, 'voxM2')
		elif caption.style%5 == 4:
			self.out = self.sst.singThisText(caption.translated, 'voxF3')
		
		while not self.sst.isAudioAvailable(self.out):
			time.sleep(1)
		
		self.sst.grabAudio(self.out, filename)
		return filename
