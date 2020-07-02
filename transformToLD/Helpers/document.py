from rdflib import Graph, Literal, RDF, URIRef, Namespace, DCTERMS
from datetime import datetime
from django.conf import settings
from historique.models import File


def document_project(project, metadata, format):
    ns = "http://localhost/{}/".format(project.project_name.replace(" ", "_"))
    g = create_graph(project.vocabularies, ns)
    triplets = create_metadata(project, metadata)
    if project.html_data:
        for table in project.html_data.tables:
            triplets += create_triplets(table.triplets)
        for paragraph in project.html_data.paragraphs:
            triplets += create_triplets(paragraph.terms)
    if project.csv_data:
        triplets += create_triplets(project.csv_data.triplets)
    if project.text_data:
        triplets += create_triplets(project.text_data.terms)
    for triple in triplets:
        g.add(triple)
    directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                  project.user_id, project.project_name)
    filename = "{}_{}_{}_{}".format(
        project.project_name, format, datetime.now(), "outputfile.rdf")
    path = directory+filename
    with open(path, "w") as output_file:
        output_file.write(g.serialize(format=format).decode("utf-8"))
    output = File(path=path, filename=filename,
                  file_type="rdf/"+format, created_at=datetime.now())
    outputs = []
    if project.output_files:
        for o in project.output_files:
            outputs.append(o)
    outputs.append(output)
    project.output_files = outputs
    project.converted = True
    project.converted_at = datetime.now()
    project.save()


def create_triplets(triplets):
    triplets_list = []
    for triple in triplets:
        s = URIRef(triple.subject)
        p = URIRef(triple.predicate)
        o = Literal(triple.object)
        triplets_list.append((s, p, o))
    return triplets_list


def create_metadata(project, metadata):
    triplets = []
    s = URIRef(
        "https://localhost/{}".format(project.project_name.replace(" ", "_")))
    p = DCTERMS.created
    o = Literal(str(datetime.now().date()))
    triplets.append((s, p, o))
    license = metadata.get('license', None)
    if license:
        p = DCTERMS.license
        o = Literal(license)
        triplets.append((s, p, o))
    creator = metadata.get('creator', None)

    if hasattr(metadata, 'creator'):
        p = DCTERMS.creator
        o = Literal(creator)
        triplets.append((s, p, o))
    subject = metadata.get('subject', None)

    if subject:
        p = DCTERMS.subject
        o = Literal(subject)
        triplets.append((s, p, o))
    title = metadata.get('title', None)

    if title:
        p = DCTERMS.title
        o = Literal(title)
        triplets.append((s, p, o))
    description = metadata.get('description', None)

    if description:
        p = DCTERMS.description
        o = Literal(description)
        triplets.append((s, p, o))
    return triplets


def create_graph(vocabularies, namespace="http://localhost/"):
    g = Graph()
    n = Namespace(namespace)
    for vocab in vocabularies:
        g.bind(vocab.prefix, vocab.uri)
    return g


def translate_file(project, format):
    g = Graph()
    src = project.output_files[-1]
    src_format = src.file_type.split("/")[-1]
    g.parse(src.path, format=src_format)
    directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                  project.user_id, project.project_name)
    filename = "{}_{}_{}_{}".format(
        project.project_name, format, datetime.now(), "outputfile.rdf")
    path = directory+filename
    with open(path, "w") as output_file:
        output_file.write(g.serialize(format=format).decode("utf-8"))

    output = File(path=path, filename=filename,
                  file_type="rdf/"+format, created_at=datetime.now())
    outputs = []
    if project.output_files:
        for o in project.output_files:
            outputs.append(o)
    outputs.append(output)
    project.output_files = outputs
    project.converted = True
    project.converted_at = datetime.now()
    project.save()
