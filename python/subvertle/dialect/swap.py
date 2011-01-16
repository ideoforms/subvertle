
class swap(dialect)
	lookup={}

	def __init__(self,map):
		self.__init__(self)
		self.makeLookup(map)

	def makeLookup(self,map):
		fd = open(map) 
		for line in fd.readlines():
			relation = split(line,'\t')
			lookup{relation[0].lower}=relation[1].lower

	def process(string):
		slang=[]
		words = split(string," ")
		for word in words:
			if (slang.has_key(word)):
				slang.append(lookup[word])
			else:
				slang.append(word)
		return string.join(slang)

