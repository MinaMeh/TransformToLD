from xml.etree import ElementTree
import requests
from .classes import Vocabulary
def getVocab(term, type="class"):
    vocab_list=[]
    URL = "https://lov.linkeddata.es/dataset/lov/api/v2/term/search?q=" + term + "&?type=" + type
    r = requests.get(URL)
    data = r.json()
    for element in data["results"]:
        vocab= Vocabulary(element["prefixedName"][0], element['vocabulary.prefix'][0], element['uri'][0], element['type'], element['score'])
        vocab_list.append(vocab)
    return vocab_list
def getTerm(term):
    uri_list=[]
    URL = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=" + term
    r= requests.get(URL)
    file = ElementTree.fromstring(r.content)
    data=file.findall("./{http://lookup.dbpedia.org/}Result/{http://lookup.dbpedia.org/}URI")
    for element in data:
        uri_list.append(element.text)
    return uri_list

