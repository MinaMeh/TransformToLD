import requests


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


def get_vocab(term, list_vocabs=None, term_type="property"):
    '''
    get vocabs returns a list of terms in the Linked Open Vocabularies for the word "term"
     having the type "term_type" in the list of vocabularies "list_vocabs" 
     example getVocab("firstName",[foaf,rdfs], "property)
    '''
    vocab_list = []
    URL = "https://lov.linkeddata.es/dataset/lov/api/v2/term/search?q=" + \
        term + "&?type=" + term_type
    r = requests.get(URL)
    data = r.json()
    for element in data["results"]:
        if (list_vocabs == [] or list_vocabs == None):
            if element["type"] == term_type:
                vocab = Property(term, element["prefixedName"][0], element['vocabulary.prefix']
                                 [0], element['uri'][0], element['type'], element['score'])
                vocab_list.append(vocab.to_dict())
        elif (element['vocabulary.prefix'][0] in list_vocabs):
            if element["type"] == term_type:
                vocab = Property(term, element["prefixedName"][0], element['vocabulary.prefix']
                                 [0], element['uri'][0], element['type'], element['score'])
                vocab_list.append(vocab.to_dict())
    return vocab_list


print(get_vocab("seeAlso", ["rdfs"]))
