from pipe import *
from xgoogle.translate import Translator



"""                                                           ||
||Afrikaans    =[af]  Haitian C  =[ht]  Serbian      =[sr]    ||
||Albaniaan    =[sq]  Hebrew     =[iw]  Slovak       =[sk]    ||
||Arabic       =[ar]  Hindi      =[hi]  Slovenian    =[sl]    ||
||Belarusian   =[be]  Hungarian  =[hu]  Spanish      =[es]    || 
||Bulgarian    =[bg]  Icelandic  =[is]  Swahili      =[sw]    ||
||Catalan      =[ca]  Indonesian =[id]  Swedish      =[sv]    || 
||Chinese Si=[zh-CN]  Irish      =[ga]  Thai         =[th]    ||
||Chinese Tr=[zh-TW]  Italian    =[it]  Thurkish     =[tr]    ||
||Czech        =[cs]  Japanese   =[ja]  Ukrainian    =[uk]    ||
||Danish       =[da]  Korean     =[ko]  Viatnamese   =[vi]    ||
||Dutch        =[nl]  Latvian    =[lv]  Welsh        =[cy]    ||
||English      =[en]  Lithuanian =[lt]  Yiddish      =[yi]    ||
||Estonian     =[et]  Macedonian =[mk]                        ||
||Filipino     =[tl]  Maltese    =[mt]                        ||
||Finnish      =[fi]  Norwegian  =[no]                        ||
||French       =[fr]  Polish     =[pl]                        ||
||Galician     =[gl]  Portuguese =[pt]                        ||
||German       =[de]  Romanian   =[ro]                        ||
||Greek        =[el]  Russian    =[ru] 
"""
class language(pipe):
	def __init__(self, parameters={}, child=None):
		pipe.__init__(self,parameters,child)
		self.pipe = "language"
		self.languages = parameters['languages'] # array of languages
		self.child = child
		self.translator = Translator()

	def translate(self,string,toLang):
		return self.translator.translate(string, lang_to=toLang)

	def transform(self, string):
		transformed = string
		for i in (range(0,len(self.languages))):
			#print "from "+self.langs[i]+" to "+self.langs[i+1]
			transformed = self.translate(transformed,self.languages[i])
		return transformed



