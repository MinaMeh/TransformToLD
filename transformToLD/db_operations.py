from historique.models import *


def update_project_tables(project, tables):
    csv_projects = []
    for table in tables:
        headers = []
        for header in table["headers"]:
            hdr = Header(name=header['name'], selected=header["selected"])
            hdr.translated = table.get("translated", None)
            hdr.combinaison = table.get("combinaison", [])

            headers.append(hdr)
        csv_prj = CsvProject(id=table['id'], selected=table['selected'],
                             lines=table["lines"], columns=table['columns'], headers=headers)
        csv_projects.append(csv_prj)
    project.html_data.tables = csv_projects
    project.save()


def update_project_paragraphs(project, paragraphs):
    text_projects = []

    for paragraph in paragraphs:
        triplets = []
        for sentence in paragraph['sentences']:
            sentence_triplets = sentence.get("triplets", [])
            if sentence_triplets != []:
                for tr in sentence_triplets:
                    triplet = Triplet(
                        subject=tr["subject"], object=tr['object'], predicate=tr['predicate'], selected=tr['selected'])
                    triplets.append(triplet)
        text_projects.append(TextProject(triplets=triplets))
    project.html_data.paragraphs = text_projects
    project.save()
