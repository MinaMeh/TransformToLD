import requests
import spacy
import json
TYPE_MAPPING= {
    "PER": "person",
    "LOC": "location",
    "ORG": "organisation",
    "MISC": "misc"
}


class Entity(object):
    def __init__(self,name, entity_type):
        self.name = name
        self.entity_type = entity_type

    def to_dict(self):
        return {
            "name": self.name,
            "entity_type": self.entity_type
     }
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

def get_vocab(term, list_vocabs=None, term_type="property"):
    '''
    get vocabs returns a list of terms in the Linked Open Vocabularies for the word "term"
     having the type "term_type" in the list of vocabularies "list_vocabs" 
     example getVocab("firstName",[foaf,rdfs], "property)
    '''
    vocab_list=[]
    URL = "https://lov.linkeddata.es/dataset/lov/api/v2/term/search?q=" + term + "&?type=" + term_type
    r = requests.get(URL)
    data = r.json()
    for element in data["results"]:
        if ( list_vocabs==None):
            vocab= Property(element["prefixedName"][0], element['vocabulary.prefix'][0], element['uri'][0], element['type'], element['score'])
            vocab_list.append(vocab.to_dict())
        elif (element['vocabulary.prefix'][0] in list_vocabs ):
            vocab= Property(element["prefixedName"][0], element['vocabulary.prefix'][0], element['uri'][0], element['type'], element['score'])
            vocab_list.append(vocab.to_dict())
    return vocab_list
def get_class(entity):
    '''
    get_class return all possible classes URIS of the entity "entity" in the vocabularies "list_vocabs"
    '''
    return TYPE_MAPPING[entity]

def get_entities(paragraph, model='xx_ent_wiki_sm'):
    '''
    extract the entities of the paragraph "paragraph" using the model "model" and map it to classes of the vocabularies 
    present in the list "vocabs_list"
    '''
    nlp = spacy.load(model)
    doc = nlp(paragraph)
    entities = [Entity(X.text, get_class(X.label_)).to_dict() for X in doc.ents]
    return entities

voc = get_entities("Bill Gates est le fondateur de Microsoft Corporation")
print(voc)
with open("test.json",'a') as file:
    json.dump(voc,file)