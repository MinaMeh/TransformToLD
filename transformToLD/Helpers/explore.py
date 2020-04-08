from xml.etree import ElementTree
import requests
from transformToLD.Classes.classes import Vocabulary, Property, Entity
import spacy

TYPE_MAPPING= {
    "PER": "person",
    "LOC": "location",
    "ORG": "organisation",
    "MISC": "misc"
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

def get_term(term):
    '''
    get_terms returns all the possible URIS of the term "term" in DBpedia
    '''
    uri_list=[]
    URL = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + term
    r= requests.get(URL)
    file = ElementTree.fromstring(r.content)
    data=file.findall("./{http://lookup.dbpedia.org/}Result/{http://lookup.dbpedia.org/}URI")
    for element in data:
        uri = {}
        uri["uri"]=element.text
        uri_list.append(uri)
    return uri_list

def get_vocab_list():
    '''
    get_vocabs_list returns the list of vocabularies in the Linked Open Vocabularies
    '''
    vocab_list=[]
    URL = "https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/list"
    r = requests.get(URL)
    data = r.json()
    vocab_list=[]
    for element in data:
        vocab= Vocabulary(element["prefix"], element['uri'], element['titles'][0]['value']).to_dict()
        vocab_list.append(vocab)
    return vocab_list

def get_class(entity, list_vocabs):
    '''
    get_class return all possible classes URIS of the entity "entity" in the vocabularies "list_vocabs"
    '''
    return get_vocab(TYPE_MAPPING[entity],list_vocabs=list_vocabs, term_type="class")

def get_entities(paragraph, vocabs_list, model='xx_ent_wiki_sm'):
    '''
    extract the entities of the paragraph "paragraph" using the model "model" and map it to classes of the vocabularies 
    present in the list "vocabs_list"
    '''
    nlp = spacy.load(model)
    doc = nlp(paragraph)
    entities = [Entity(X.text, get_class(X.label_,vocabs_list), get_term(X.text)).to_dict() for X in doc.ents]
    return entities
    
    