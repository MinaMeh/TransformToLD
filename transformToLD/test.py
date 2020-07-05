# from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode
# from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
#     PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
#     VOID, XMLNS, XSD

# g = Graph()
# g.bind("foaf", FOAF)
# amina = URIRef("https://localhost/amina")
# imene = Literal("imene")
# youcef = Literal("youcef")
# n = Namespace("http://example.org/people/")
# pr = URIRef("http://xmlns.com/foaf/0.1/knows")
# g.add((amina, FOAF.knows, imene))
# g.add((amina, FOAF.knows, youcef))
# print(g.serialize(format="xml").decode("utf-8"))
import textrazor


def concatenate(word_list):
    term = ""
    for word in word_list:
        term += " " + word.token
    return term


textrazor.api_key = "4599791ae63e2fb4f39d911a2145db56469b306ba8fbd6eda53e65ce"
client = textrazor.TextRazor(extractors=['entities', 'relations'])
p = '''
Bill Gates is is an American business magnate, software developer, investor, and philanthropist.
He is best known as the co-founder of Microsoft Corporation.
During his career at Microsoft, Gates held the positions of chairman, chief executive officer (CEO, president and chief software architect, while also being the largest individual shareholder until May 2014. He is one of the best-known entrepreneurs and pioneers of the microcomputer revolution of the 1970s and 1980s.
Maria knows Alfred, they worked together in Google when they were developpers
'''
response = client.analyze(p)
for sentence in response.sentences():
    print(concatenate(sentence.words))
