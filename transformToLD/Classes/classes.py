class Property():
    def __init__(self, term, prefixedName, vocabPrefix, uri, type, score):
        self.prefixedName = prefixedName
        self.vocabprefix = vocabPrefix
        self.uri = uri
        self.type = type
        self.score = score
        self.term = term

    def to_dict(self):
        return {
            "term": self.term,
            "prefixedName": self.prefixedName,
            "vocabPrefix": self.vocabprefix,
            "uri": self.uri,
            "type": self.type,
            "score": self.score
        }


class Vocabulary(object):
    def __init__(self, prefix, uri, title):
        self.prefix = prefix
        self.uri = uri
        self.title = title

    def to_dict(self):
        return {
            "prefix": self.prefix,
            "uri": self.uri,
            "title": self.title
        }


class Tag(object):
    def __init__(self, word, tag):
        self.word = word
        self.tag = tag

    def to_dict(self):
        return {
            "word": self.word,
            "tag": self.tag
        }
