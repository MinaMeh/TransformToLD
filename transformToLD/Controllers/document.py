from rdflib import Graph, Literal, RDF, RDFS, URIRef, Namespace, DCTERMS, XSD, OWL
from datetime import datetime
from django.conf import settings
from historique.models import File, MetaData, Triplet
import pandas as pd
DATATYPES = {
    "xsd:int": XSD.integer,
    "xsd:float": XSD.float,
    "xsd:string": XSD.string,
    "xsd:boolean": XSD.boolean,
    "xsd:date": XSD.date
}


def document_project(project, metadata, format):
    ns = "http://localhost/{}/".format(project.project_name.replace(" ", "_"))
    g = create_graph(project.vocabularies, ns)
    directory = "{}{}/{}/".format(settings.MEDIA_URL,
                                  project.user_id, project.project_name)
    filename = "{}_{}_{}_{}".format(
        project.project_name, format, datetime.now(), "outputfile.rdf")
    path = directory+filename.replace(':', "_")
    with open(path, "w") as output_file:
        create_metadata(project, metadata, output_file, format, g)
        create_properties(project, output_file, format, g)
        if project.html_data:
            create_html_classes(project, g)
            for table in project.html_data.tables:
                if table.selected:
                    create_triplets(table.triplets, project,
                                    output_file, format, g)
            for paragraph in project.html_data.paragraphs:
                if paragraph.terms:
                    create_triplets(paragraph.terms, project,
                                    output_file, format, g)
        if project.csv_data:
            create_triplets(project.csv_data.triplets,
                            project, output_file, format, g)
            create_class(project, g)
        if project.text_data:
            create_triplets(project.text_data.terms,
                            project, output_file, format, g)
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


def create_properties(project, output_file, format, g):
    triplets = []
    ns = "http://localhost/{}/".format(project.project_name.replace(" ", "_"))

    if project.properties:
        for prop in project.properties:
            s = URIRef(ns+prop.label)
            p = RDF.type
            o = RDF.Property
            triplets.append((s, p, o))
            p = RDFS.label
            o = Literal(prop.label, datatype=XSD.string)
            triplets.append((s, p, o))
            p = RDFS.comment
            o = Literal(prop.comment, datatype=XSD.string)
            triplets.append((s, p, o))
            if prop.subPropertyOf:
                p = RDFS.subPropertyOf
                o = URIRef(prop.subPropertyOf)
                triplets.append((s, p, o))
    for triplet in triplets:
        g.add(triplet)


def create_triplets(triplets, project, output_file, format, g):
    triplets_list = []
    try:
        print("path", triplets.path)
        triplets_df = pd.read_csv(triplets.path)
    except FileNotFoundError:
        return
    ns = "http://localhost/{}/".format(project.project_name.replace(" ", "_"))
    for _, triple in triplets_df.iterrows():
        s = URIRef(triple['subject'].replace(" ", ''))
        if hasattr(triple, 'subject_uri') and 'http' in str(triple['subject_uri']):
            p = URIRef(RDFS.seeAlso)
            o = URIRef(triple['subject_uri'])
            triplets_list.append((s, p, o))
        if hasattr(triple, 'object_uri') and triple["object_type"] == 'url':
            s_s = URIRef(triple['object'])
            s_p = URIRef(RDFS.seeAlso)
            s_o = URIRef(triple['object_uri'])
            triplets_list.append((s_s, s_p, s_o))

        if "http" not in triple['predicate']:
            triple['predicate'] = ns+triple['predicate'].split(":")[-1]
        p = URIRef(triple['predicate'].replace(" ", ""))
        if triple["object_type"] == 'url':
            o = URIRef(triple['object'])
        else:
            o = Literal(triple.object,
                        datatype=DATATYPES[triple["object_type"]])
        triplets_list.append((s, p, o))
    for triplet in triplets_list:
        g.add(triplet)


def create_class(project, g):
    ns = "http://localhost/{}/".format(project.project_name.replace(" ", "_"))
    if hasattr(project.csv_data.row_class, "label"):
        triplets = []
        rdf_class = project.csv_data.row_class
        s = URIRef(ns+rdf_class.label)
        p = RDF.type
        o = RDFS.Class
        g.add((s, p, o))
        p = RDFS.label
        o = Literal(rdf_class.label, datatype=XSD.string)
        g.add((s, p, o))
        p = RDFS.comment
        o = Literal(rdf_class.comment, datatype=XSD.string)
        g.add((s, p, o))
        if rdf_class.subClassOf:
            p = RDFS.subClassOf
            o = URIRef(rdf_class.subClassOf)
            g.add((s, p, o))


def create_html_classes(project, g):
    ns = "http://localhost/{}/".format(
        project.project_name.replace(" ", "_"))
    for table in project.html_data.tables:
        if hasattr(table.row_class, "label"):
            triplets = []
            rdf_class = table.row_class
            s = URIRef(ns+rdf_class.label)
            p = RDF.type
            o = RDFS.Class
            g.add((s, p, o))
            p = RDFS.label
            o = Literal(rdf_class.label, datatype=XSD.string)
            g.add((s, p, o))
            p = RDFS.comment
            o = Literal(rdf_class.comment, datatype=XSD.string)
            g.add((s, p, o))
            if rdf_class.subClassOf:
                p = RDFS.subClassOf
                o = URIRef(rdf_class.subClassOf)
                g.add((s, p, o))


def create_metadata(project, metadata, output_file, format, g):
    triplets = []
    s = URIRef(
        "http://localhost/{}/".format(project.project_name.replace(" ", "_")))
    p = DCTERMS.created
    o = Literal(str(datetime.now().date()), datatype=XSD.date)
    triplets.append((s, p, o))
    license = metadata.get('license', None)
    if license:
        p = DCTERMS.license
        o = Literal(license, datatype=XSD.string)
        triplets.append((s, p, o))
    creator = metadata.get('creator', None)
    if creator:
        p = DCTERMS.creator
        o = Literal(creator, datatype=XSD.string)
        triplets.append((s, p, o))
    subject = metadata.get('subject', None)

    if subject:
        p = DCTERMS.subject
        o = Literal(subject, datatype=XSD.string)
        triplets.append((s, p, o))
    title = metadata.get('title', None)

    if title:
        p = DCTERMS.title
        o = Literal(title, datatype=XSD.string)
        triplets.append((s, p, o))
    description = metadata.get('description', None)

    if description:
        p = DCTERMS.description
        o = Literal(description, datatype=XSD.string)
        triplets.append((s, p, o))
    project.metadata = MetaData(creator=creator, createdAt=datetime.now(
    ).date(), description=description, title=title, subject=subject, license=license)
    project.save()
    for triplet in triplets:
        g.add(triplet)


def create_graph(vocabularies, namespace="http://localhost/"):
    g = Graph()
    n = Namespace(namespace)
    g.bind("dataset", n)
    g.bind("dcterms", DCTERMS)
    if vocabularies is not None:
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
    path = directory+filename.replace(":", "_")
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
