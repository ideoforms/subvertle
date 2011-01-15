
class expletive (dialect):
    def __init__(self):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        self.tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())

    def process(self, text):
        tokenized = self.tokenizer.tokenize(text)
        tagged = self.tagger.tag(tokenized)

        done = {}
        for word, type in tagged:
            if word in done:
                continue
            # # # print "%s: %s" % (type, word)
            if type and type[0] == 'N' and random.random() < 0.4:
                text = re.sub(r"\b%s\b" % word, "fucking %s" % word, text)
                done[word] = 1

        return text


