from subdialect import *

class subtranslate():
    def __init__(self, dialectName):
        self.dialect = dialectName # expletive()

    def process(self, string):
        return self.dialect.process(string)
