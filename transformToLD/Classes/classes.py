class Property():
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

class Vocabulary(object):
    def __init__(self,prefix, uri,title):
        self.prefix = prefix
        self.uri = uri
        self.title = title

    def to_dict(self):
        return {
            "prefix": self.prefix,
            "uri": self.uri,
            "title": self.title
        }

class Entity(object):
    def __init__(self,name, entity_type, uri):
        self.name = name
        self.entity_type = entity_type
        self.uri= uri

    def to_dict(self):
        return {
            "name": self.name,
            "entity_type": self.entity_type,
            "uri": self.uri
     }