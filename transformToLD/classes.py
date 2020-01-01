class Vocabulary():
    def __init__(self,prefixedName, vocabPrefix,uri,type,score):
        self.prefixedName = prefixedName
        self.vocabprefix = vocabPrefix
        self.uri = uri
        self.type = type
        self.score = score

    def to_dict(self):
        return {
            "prefixedName": self.prefixedName,
            "vocabPrefix": self.vocabprefix,
            "uri": self.uri,
            "type": self.type,
            "score": self.score
        }
