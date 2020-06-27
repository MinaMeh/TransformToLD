import pandas as pd


def convert_csv(file_name, delimiter, terms):
    file = pd.read_csv("media/"+file_name, delimiter=delimiter)
    lines = []
    domain_name = "localhost/dataset/#"
    for index, row in file.iterrows():
        for term in terms:
            line = dict()
            line["subject"] = domain_name + str(index)
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
