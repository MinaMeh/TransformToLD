from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
    PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
    VOID, XMLNS, XSD

g = Graph()
g.bind("foaf", FOAF)
amina = URIRef("https://localhost/amina")
imene = Literal("imene")
youcef = Literal("youcef")
n = Namespace("http://example.org/people/")
pr = URIRef("http://xmlns.com/foaf/0.1/knows")
g.add((amina, FOAF.knows, imene))
g.add((amina, FOAF.knows, youcef))
print(g.serialize(format="xml").decode("utf-8"))
# bob = URIRef("http://example.org/people/Bob")
# linda = BNode()  # a GUID is generated

# name = Literal('Bob')  # passing a string
# age = Literal(24)  # passing a python int
# height = Literal(76.5)  # passing a python float
# n = Namespace("http://example.org/people/")

# n.bob  # = rdflib.term.URIRef(u'http://example.org/people/bob')
# n.eve  # = rdflib.term.URIRef(u'http://example.org/people/eve')
# g.bind("foaf", FOAF)

# g.add((bob, RDF.type, FOAF.Person))
# g.add((bob, FOAF.name, name))
# g.add((bob, FOAF.knows, linda))
# g.add((linda, RDF.type, FOAF.Person))
# g.add((linda, FOAF.name, Literal("Linda")))

# print(g.serialize(format="xml").decode("utf-8"))
