from xml.etree import ElementTree
import requests
from transformToLD.Classes.classes import Vocabulary, Property


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
        if (list_vocabs == None):
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


def get_term(term):
    '''
    get_terms returns all the possible URIS of the term "term" in DBpedia
    '''
    uri_list = []
    URL = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + term
    r = requests.get(URL)
    file = ElementTree.fromstring(r.content)
    data = file.findall(
        "./{http://lookup.dbpedia.org/}Result/{http://lookup.dbpedia.org/}URI")
    for element in data:
        uri = {}
        uri["uri"] = element.text
        uri_list.append(uri)
    return uri_list


def get_vocab_list():
    '''
    get_vocabs_list returns the list of vocabularies in the Linked Open Vocabularies
    '''
    vocab_list = []
    URL = "https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/list"
    r = requests.get(URL)
    data = r.json()
    vocab_list = []
    for element in data:
        vocab = Vocabulary(
            element["prefix"], element['uri'], element['titles'][0]['value']).to_dict()
        vocab_list.append(vocab)
    return vocab_list


def explore_csv(columns, vocabs_list):
    '''
    Map csv columns to LOV terms
    '''
    terms = []
    for col in columns:
        terms.append(explore_column(col, vocabs_list))

    return terms


def explore_column(column, vocabs_list):
    """
    Get column terms in the LOV cloud
    """
    term = {}
    transated = column["translated"]
    combinaisons = column["combinaison"]
    term["property"] = column['name']
    term["selected"] = ""

    term["result"] = []
    for comb in combinaisons:
        data = get_vocab(comb, vocabs_list, 'property')
        term["result"] += data
    term['result'].sort(key=lambda term: term.get('score'), reverse=True)
    return term


def explore_paragraph(paragraph, vocab_list):
    terms = []
    for sentence in paragraph['sentences']:
        for triplet in sentence['triplets']:
            if triplet["selected"] == True:
                term = {}
                term["property"] = triplet['predicate']
                term["selected"] = ""
                term["result"] = get_vocab(triplet['predicate'], vocab_list)
                term['result'].sort(
                    key=lambda term: term.get('score'), reverse=True)
                terms.append(term)
    paragraph['terms'] = terms
    return paragraph
