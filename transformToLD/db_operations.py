from historique.models import *
from django.conf import settings
from datetime import datetime


def update_project_tables(project, tables=None, triplets=None, headers=None):
    if tables:
        csv_projects = []
        for table in tables:
            hdrs = []
            for header in table["headers"]:
                hdr = Header(name=header['name'], selected=header["selected"])
                hdr.translated = header.get("translated", 'test')
                hdr.combinaison = header.get("combinaison", [])
                hdrs.append(hdr)
            csv_prj = CsvProject(id=table['id'], selected=table['selected'],
                                 lines=table["lines"], columns=table['columns'], headers=hdrs)
            csv_projects.append(csv_prj)
        project.html_data.tables = csv_projects
    if headers:
        for table in project.html_data.tables:
            for tr_table in headers:
                if tr_table["id"] == table.id:
                    rdf_class = tr_table.get("rowClass", None)
                    if rdf_class:
                        if rdf_class["new"]:
                            new_class = RdfClass(
                                label=rdf_class["label"], comment=rdf_class["comment"], subClassOf=rdf_class['subClassOf'])
                        else:
                            new_class = RdfClass(uri=rdf_class["uri"])
                        table.row_class = new_class
                    headers_id = tr_table.get("rowId", None)
                    if headers_id:
                        h_ids = [Header(name=h["property"])
                                 for h in headers_id]
                        table.headers_id = h_ids

                    for term in tr_table['terms']:
                        hdrs = table.headers
                        for head in hdrs:
                            if head.name == term['property']:
                                if term["term"]["uri"]:
                                    head.term = term["term"]["uri"]

    if triplets:
        for table in project.html_data.tables:
            directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                          project.user_id, project.project_name)
            filename = "{}_{}_{}".format(
                project.project_name, "triplets_file", table.id)
            file_path = directory+filename
            table.triplets = File(path=file_path, filename=filename,
                                  file_type="csv", created_at=datetime.now())
    project.save()


def update_project_paragraphs(project, paragraphs=None, terms=None):
    if paragraphs:
        text_projects = []
        for paragraph in paragraphs:
            directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                          project.user_id, project.project_name)
            filename = "{}_{}_{}_{}".format(
                project.project_name, "realtions_file", 'paragraph', paragraph['id'])
            file_path = directory+filename
            triplets = File(path=file_path, filename=filename,
                            file_type="csv", created_at=datetime.now())
            text_projects.append(TextProject(triplets=triplets))
        project.html_data.paragraphs = text_projects
    if terms:
        for paragraph in project.html_data.paragraphs:
            directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                          project.user_id, project.project_name)
            filename = "{}_{}_{}_{}".format(
                project.project_name, "triplets_file", 'paragraph', paragraph.id)
            file_path = directory+filename
            paragraph.terms = File(path=file_path, filename=filename,
                                   file_type="csv", created_at=datetime.now())

    project.save()


def update_csv_project(project, headers=None, triplets=None):
    if headers:
        hdrs = []
        for header in headers:
            hdr = Header(name=header['name'], selected=header["selected"])
            hdr.translated = header.get("translated", 'test')
            hdr.combinaison = header.get("combinaison", [])
            hdrs.append(hdr)
        project.csv_data.headers = hdrs
    if triplets:
        triples = []
        for triplet in triplets:
            trpl = Triplet(
                subject=triplet["subject"], object=triplet['object'], predicate=triplet['predicate'])
            triples.append(trpl)
        project.csv_data.triplets = triples
    project.save()


def update_text_project(project, terms=None, triplets=None):
    if triplets:
        directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                      project.user_id, project.project_name)
        filename = "{}_{}".format(project.project_name, "triplets_file")
        file_path = directory+filename
        triplets = File(path=file_path, filename=filename,
                        file_type="csv", created_at=datetime.now())

        project.text_data = TextProject(triplets=triplets)
    if terms:
        directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                      project.user_id, project.project_name)
        filename = "{}_{}".format(project.project_name, "triplets_file")
        file_path = directory+filename
        terms = File(path=file_path, filename=filename,
                     file_type="csv", created_at=datetime.now())
        project.text_data.terms = terms
    project.save()
