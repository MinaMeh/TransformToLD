import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib import RDF
from django.conf import settings
from historique.models import RdfClass


def convert_csv(project, file_name, delimiter, terms, headers_id=None, row_class=None):
    file = pd.read_csv(project.input_file.path, delimiter=delimiter)
    file.fillna('')
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


def convert_text(triplets, terms, project):
    lines = []
    terms_dict = dict()
    domaine_name = "http://localhost/{}/".format(
        project.project_name.replace(" ", "_"))
    domaine_name = "http://localhost/dataset/"
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
        line = dict()
        headers_id = table.get("rowId", None)
        if headers_id:
            h_ids = [h["property"] for h in headers_id]

            subject = "_".join([str(row[head]) for head in h_ids])
        else:
            subject = str(index)
        line["subject"] = domain_name+subject
        row_class = table.get("rowClass", None)
        if row_class:
            if row_class["new"] == False:
                row_type = row_class["uri"]
            else:
                row_type = domain_name+row_class['label']
            line["predicate"] = str(RDF.type)
            line['object'] = row_type
            lines.append(line)

        for term in table["terms"]:
            line = dict()
            line["subject"] = domain_name+subject
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
