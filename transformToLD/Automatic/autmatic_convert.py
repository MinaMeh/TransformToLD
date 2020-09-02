from django.core.files.storage import FileSystemStorage
import os
from rest_framework.response import Response
from rest_framework import status, serializers
from django.conf import settings
from transformToLD.Controllers.extract import *
from transformToLD.Controllers.preprocess import *
from transformToLD.Controllers.explore import *
from transformToLD.Controllers.convert import *
from transformToLD.Controllers.document import *
from transformToLD.db_operations import *
from historique.models import *
from linkeddata.settings_folder import dev_setting
import time
from linkeddata.wsgi import *
from shutil import copyfile


def auto_convert_csv(file_path, project_name, separator=","):
    ###########EXTRACT##############
    print("extract")
    record = dict()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "linkeddata.settings_folder.dev_setting")
    directory = "{}/0/{}".format(settings.MEDIA_URL,
                                 project_name)
    try:
        os.makedirs(directory)
    except FileExistsError:
        return "error making dir"

    filename = os.path.basename(file_path)

    upload_file = "{}/{}".format(directory, filename)
    copyfile(file_path, upload_file)
    input_file = File(path=upload_file,
                      filename=filename, file_type='csv')

    project = Project(project_name=project_name,
                      input_file=input_file, user_id=0)
    t1 = time.time()
    results = extract_csv_data(upload_file, separator)
    t2 = time.time()
    extract_time = t2-t1
    record["extract"] = extract_time
    record['nb_rows'] = results['lines']
    record["nb_cols"] = results['columns']
    print("extractt = {} s".format(extract_time))
    resp = {'results': results, 'filename': filename,
            'type': 'csv'}
    csv_data = CsvProject(separator=separator,
                          columns=results['columns'], lines=results['lines'])
    project.csv_data = csv_data
    project.save()
    print("preprocess")
    ##############Preprocess #################
    columns = results["headers"]
    t1 = time.time()
    headers = preprocess_columns(columns)
    t2 = time.time()
    preprocess_time = t2-t1
    print("preprocess = {} s".format(preprocess_time))
    record['preprocess'] = preprocess_time
    update_csv_project(project, headers=headers)
    resp = {'columns_selected': columns,
            "headers": headers}
    ##########Mapping#################
    print("Map")
    terms = []
    t_start = time.time()
    for col in headers:
        if col['selected'] == True:
            terms.append(explore_column(col, vocabs_list=None))
    t_end = time.time()
    map_time = t_end-t_start
    print("map = {} s".format(map_time))
    record['map'] = map_time
    resp = {"terms": terms, 'execution_time': map_time}
    ####Convert######
    print("convert")

    for term in terms:
        headers = project.csv_data.headers
        if term['result'] == []:
            properiety = Propriety(
                label=term['property'], comment='this is a property to describe{}'.format(term['property']), uri="http://localhost/{}".format(project_name))
            if project.properties is None:
                project.properties = [properiety]
            else:
                project.properties.append(properiety)
            project.save()
            prop = dict(label=term['property'], comment='this is a property to describe  {}'.format(
                term['property']), uri="http://localhost/{}".format(project_name))
            term['term'] = prop
            print(prop)
        else:
            term['term'] = term['selected']
        for head in headers:
            if head.name == term['property']:
                if term["term"]["uri"]:
                    head.term = term["term"]["uri"]
    project.save()
    t_start = time.time()
    lines = convert_csv(project, filename, separator,
                        terms)
    t_end = time.time()
    convert_time = t_end-t_start
    record['convert'] = convert_time
    record["nb_triplets"] = len(lines)
    print("convert= {} s".format(convert_time))
    metadata = {"title": project_name}
    print("document")
    record["exec_time"] = extract_time+preprocess_time+map_time+convert_time
    document_project(project, metadata, "turtle")
    return record


def auto_convert_text(file_path, project_name):
    ###########EXTRACT##############
    print("extract")
    record = dict()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "linkeddata.settings_folder.dev_setting")
    directory = "{}/0/{}".format(settings.MEDIA_URL,
                                 project_name)
    try:
        os.makedirs(directory)
    except FileExistsError:
        return "error making dir"

    filename = os.path.basename(file_path)

    upload_file = "{}/{}".format(directory, filename)
    copyfile(file_path, upload_file)
    input_file = File(path=upload_file,
                      filename=filename, file_type='csv')

    project = Project(project_name=project_name,
                      input_file=input_file, user_id=0)
    t1 = time.time()
    results = extract_text_data(upload_file)
    t2 = time.time()
    extract_time = t2-t1
    print("extract time {}".format(extract_time))
    record["extract"] = extract_time
    record['nb_sentences'] = len(results['sentences'])
    print("nb_phrases {}".format(len(results['sentences'])))

    ###########Preprocess#########################
    paragraph = {"paragraph": results.get(
        'paragraph', 'nthg'), "sentences": results.get('sentences', 'nthg')}
    t_start = time.time()
    paragraph = preprocess_paragraph(project, paragraph)
    t_end = time.time()
    preprocess_time = t_end-t_start
    record['preprocess'] = preprocess_time
    print("preprorcess time {}".format(preprocess_time))
    #############Mapping#############
    t_start = time.time()
    paragraph = explore_paragraph(paragraph)
    t_end = time.time()
    map_time = t_end-t_start
    resp = ({"data": paragraph, 'execution_time': map_time})
    record['map'] = map_time
    print("mapping time {}".format(map_time))
    #################Convert###################
    for term in paragraph['terms']:
        if term['result'] == []:
            properiety = Propriety(
                label=term['property'], comment='this is a property to describe{}'.format(term['property']), uri="http://localhost/{}".format(project_name))
            if project.properties is None:
                project.properties = [properiety]
            else:
                project.properties.append(properiety)
            project.save()
            prop = dict(label=term['property'], comment='this is a property to describe  {}'.format(
                term['property']), uri="http://localhost/{}".format(project_name))
            term['term'] = prop
            print(prop)
        else:
            term['term'] = term['selected']

    terms = [{"property": term['property'],
              "term": term['term'],
              } for term in paragraph['terms']]

    triplets = []
    for sentence in paragraph['sentences']:
        triplets += sentence['triplets']
    t_start = time.time()
    lines = convert_text(triplets, terms, project)
    t_end = time.time()
    convert_time = t_end-t_start
    update_text_project(project, terms=lines, triplets=triplets)
    resp = ({"data": lines, 'execution_time': convert_time})
    record['convert'] = convert_time
    print("convert time {}".format(convert_time))
    record['nb_triplets'] = len(lines)
    ###############Document ################
    metadata = {"title": project_name}
    print("document")
    record["exec_time"] = extract_time+preprocess_time+map_time+convert_time
    document_project(project, metadata, "turtle")
    return record


def auto_convert_html(file_path, project_name):
    print("extract")
    record = dict()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "linkeddata.settings_folder.dev_setting")
    directory = "{}/0/{}".format(settings.MEDIA_URL,
                                 project_name)
    try:
        os.makedirs(directory)
    except FileExistsError:
        return "error making dir"

    filename = os.path.basename(file_path)

    upload_file = "{}/{}".format(directory, filename)
    copyfile(file_path, upload_file)
    input_file = File(path=upload_file,
                      filename=filename, file_type='csv')

    project = Project(project_name=project_name,
                      input_file=input_file, user_id=0)
    t1 = time.time()
    results = extract_html_data(
        upload_file, extract_tables=True, extract_paragraphs=True)

    t2 = time.time()
    extract_time = t2-t1
    print("extract time {}".format(extract_time))
    record["extract"] = extract_time
    record['nb_tables'] = results['num_tables']
    record['nb_paragraphs'] = results['num_paragraphs']

    print("tables {}".format(record['nb_tables']))
    print("paragraphes {}".format(record['nb_paragraphs']))
    return record
