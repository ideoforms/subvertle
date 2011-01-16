
class cockny(dialect)
	lookup={}

	def __init__(self):
		self.__init__(self)
		self.makeLookup()

	def makeLookup(self):
		fd = open("cockney.dat") 
		for line in fd.readlines():
			relation = split(line,'\t')
			lookup{relation[1].lower}=relation[0].lower

	def process(string):
		slang=[]
		words = split(string," ")
		for word in words:
			if (slang.has_key(word)):
				slang.append(lookup[word])
			else:
				slang.append(word)
		return string.join(slang)

