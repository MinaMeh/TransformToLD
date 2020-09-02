import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib import RDF
from django.conf import settings
from historique.models import RdfClass, File
import csv
from datetime import datetime
from transformToLD.Controllers.explore import get_vocab


def convert_csv(project, file_name, delimiter, terms, headers_id=None, row_class=None):
    file = pd.read_csv(project.input_file.path, delimiter=delimiter,)
    file.fillna('not mentionned', inplace=True)
    lines = []
    directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                  project.user_id, project.project_name)
    filename = "{}_{}".format(project.project_name, "triplets_file")
    file_path = directory+filename
    triplet_file = open(file_path, "w")
    writer = csv.DictWriter(triplet_file, fieldnames=[
                            "subject", "predicate", "object", "object_type"])
    writer.writeheader()
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
            line["object_type"] = "url"
            lines.append(line)
            writer.writerow(line)
        for term in terms:
            line = dict()
            line["subject"] = domain_name+subject
            line["predicate"] = term["term"]["uri"]
            line['object'] = row[term['property']]
            line["object_type"] = term["type"]
            lines.append(line)
            writer.writerow(line)
    project.csv_data.triplets = File(
        path=file_path, filename=filename, file_type="csv", created_at=datetime.now())
    project.save()
    return lines


def convert_text(triplets, terms, entities, project, id=None):
    lines = []
    terms_dict = dict()
    entities_dict = dict()
    directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                  project.user_id, project.project_name)
    if id is not None:
        filename = "{}_{}_{}_{}".format(
            project.project_name, "triplets_file", 'paragraph', id)
    else:
        filename = "{}_{}".format(project.project_name, "triplets_file")
    file_path = directory+filename
    triplet_file = open(file_path, "w")
    writer = csv.DictWriter(triplet_file, fieldnames=[
                            "subject", 'subject_uri', "predicate", "object", 'object_uri', "object_type"])

    writer.writeheader()

    domaine_name = "http://localhost/{}/".format(
        project.project_name.replace(" ", "_"))
    for entity in entities:
        entities_dict[entity['text'].strip()] = entity['selected'].strip()
    for term in terms:
        terms_dict[term['property']] = term['term']['uri']
    for triplet in triplets:
        if triplet["selected"]:
            line = dict()
            line["subject"] = domaine_name + \
                triplet["subject"].strip().replace(' ', '_')
            try:
                line["subject_uri"] = entities_dict[triplet["subject"].strip()]
                see_also = {}
                see_also['subject'] = line["subject"]
                see_also['predicate'] = get_vocab(
                    "seeAlso", ["rdfs"])[0]['uri']
                see_also['object_type'] = "url"

                see_also['object'] = line["subject_uri"]
                lines.append(see_also)
            except KeyError:
                pass
            line["predicate"] = terms_dict[triplet["predicate"]]
            try:
                line["object_uri"] = entities_dict[triplet["object"].strip()]
                see_also_o = {}
                see_also_o['subject'] = domaine_name + \
                    triplet["object"].strip().replace(' ', '_')
                see_also_o['predicate'] = get_vocab(
                    "seeAlso", ["rdfs"])[0]['uri']
                see_also_o['object_type'] = "url"
                see_also_o['object'] = line["object_uri"]
                line['object_type'] = "url"
                line['object'] = domaine_name + \
                    triplet['object'].strip().replace(' ', '_')
                lines.append(see_also_o)
            except KeyError:
                line["object"] = triplet['object']
                line['object_type'] = "xsd:string"
            lines.append(line)
            writer.writerow(line)
    return lines


def convert_html(table, project):
    try:
        file = pd.read_html(table['filename'])[0]
    except BaseException:
        file = pd.read_csv(table['filename'])
    lines = []
    domain_name = "http://localhost/{}/".format(
        project.project_name.replace(' ', "_"))
    directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                  project.user_id, project.project_name)
    filename = "{}_{}_{}".format(
        project.project_name, "triplets_file", table["id"])
    file_path = directory+filename
    triplet_file = open(file_path, "w")
    writer = csv.DictWriter(triplet_file, fieldnames=[
                            "subject", "predicate", "object", "object_type"])
    writer.writeheader()
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
            line['object_type'] = 'url'
            lines.append(line)
            writer.writerow(line)
        for term in table["terms"]:
            line = dict()
            line["subject"] = domain_name+subject
            line["predicate"] = term["term"]["uri"]
            line['object'] = row[term['property']]
            line['object_type'] = term["type"]
            lines.append(line)
            writer.writerow(line)
    triplet_file.close()
    return lines


def create_graph(vocabularies, namespace="http://localhost/"):
    g = Graph()
    n = Namespace(namespace)
    for vocab in vocabularies:
        g.bind(vocab.prefix, vocab.uri)
    return g
