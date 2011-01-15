

class subtitle:
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
