import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib import RDF
from django.conf import settings
from historique.models import RdfClass


def convert_csv(project, file_name, delimiter, terms, headers_id=None, row_class=None):
    file = pd.read_csv("media/"+file_name, delimiter=delimiter)
    lines = []
    domain_name = "http://localhost/{}/".format(
        project.project_name.replace(' ', "_"))
    vocabs = project.vocabularies
    for index, row in file.iterrows():
        line = dict()
        if headers_id:
            subject = "_".join([str(row[head]) for head in headers_id])
        else:
            subject = str(index)
        line["subject"] = domain_name+subject
        if row_class:
            uri = row_class.get('uri', None)
            if uri:
                project.row_class = RdfClass(uri=row_class["uri"])
                row_type = row_class["uri"]
            else:
                project.row_class = RdfClass(
                    label=row_class['class']["label"], comment=row_class['class']['comment'], subClassOf=row_class['class']["subClassOf"])
                row_type = domain_name+row_class['class']['label']
            project.save()
            line["predicate"] = str(RDF.type)
            line['object'] = row_type
            lines.append(line)
        for term in terms:
            line = dict()
            line["subject"] = domain_name+subject
            line["predicate"] = term["term"]["uri"]
            line['object'] = row[term['property']]
            lines.append(line)

    return lines


def convert_text(triplets, terms):
    lines = []
    terms_dict = dict()
    domaine_name = "localhost/dataseet/"
    for term in terms:
        terms_dict[term['property']] = term['term']['uri']
    for triplet in triplets:
        if triplet["selected"]:
            line = dict()
            line["subject"] = domaine_name + triplet["subject"]
            line["predicate"] = terms_dict[triplet["predicate"]]
            line["object"] = triplet['object']
            lines.append(line)
    return lines


def convert_html(table):
    file = pd.read_html(table['filename'])[0]
    lines = []
    domain_name = "localhost/dataset/#"
    for index, row in file.iterrows():
        for term in table["terms"]:
            line = dict()
            line["subject"] = domain_name + str(index)
            line["predicate"] = term["term"]["uri"]
            line['object'] = row[term['property']]
            lines.append(line)
    return lines


def create_graph(vocabularies, namespace="http://localhost/"):
    g = Graph()
    n = Namespace(namespace)
    for vocab in vocabularies:
        g.bind(vocab.prefix, vocab.uri)
    return g
