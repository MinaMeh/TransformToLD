import os
import os
import io
import time
import csv
import json
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework import viewsets, static, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from wsgiref.util import FileWrapper
from .Serializers import VocabularySerializer, ProjectSerializer
from transformToLD.models import MyUser
from historique.models import *
from historique.serializers import ProjectSerializer, PropertySerializer, ClassSerializer
from transformToLD.Controllers.extract import extract_text_data, extract_csv_data, extract_html_data, extract_pdf_data, extract_image_data
from transformToLD.Controllers.explore import get_vocab_list, explore_csv, explore_column, get_vocab, explore_paragraph
from transformToLD.Controllers.preprocess import preprocess_columns, preprocess_paragraph
from transformToLD.Controllers.convert import convert_csv, convert_text, convert_html
from .Controllers.document import document_project, translate_file
from .db_operations import *


@api_view(['GET'])
def get_file(request):
    filepath = request.GET.get("file_path")
    file = open(filepath)
    response = HttpResponse(FileWrapper(file))
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'test.html'

    return response


@ api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def listVocabs(request):
    vocabs = get_vocab_list()
    results = VocabularySerializer(vocabs, many=True).data
    return Response(results)


@ api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def extract(request):
    file = request.FILES['file']
    separator = request.POST.get('separator')
    user_id = request.POST.get("user_id", 0)
    tables = True if request.POST.get('tables') == 'true' else False
    paragraphs = True if request.POST.get('paragraphs') == 'true' else False
    project = json.loads(request.POST.get("project"))
    project_name = project.get("project_name", "automatic-project")
    if project_name == "automatic":
        project_name = "{}_{}".format(project_name, int(time.time()))
        project['project_name'] = project_name

    directory = "{}{}/{}".format(settings.MEDIA_URL,
                                 user_id, project_name)
    try:
        os.makedirs(directory)
    except FileExistsError:
        return Response({"msg": "project already exists"}, status=status.HTTP_400_BAD_REQUEST)
    fs = FileSystemStorage(location=directory)

    filename = fs.save(file.name, file)
    upload_file = "{}/{}".format(directory, filename)
    file_type = file.content_type
    input_file = {"path": upload_file,
                  "filename": filename, "file_type": file_type}
    project["input_file"] = input_file
    project_serializer = ProjectSerializer(data=project)

    if project_serializer.is_valid():
        project_serializer.save()
        project_id = project_serializer.data['id']
    else:
        return Response({"msg": project_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    project = Project.objects.get(pk=project_id)
    if file_type == 'text/csv' or file_type == "application/vnd.ms-excel":
        t_start = time.time()
        results = extract_csv_data(upload_file, separator)
        t_end = time.time()
        exec_time = t_end-t_start
        resp = {'results': results, 'filename': filename,
                'type': 'csv', 'size': file.size, 'project_id': project_id, 'execution_time': exec_time}
        csv_data = CsvProject(separator=separator,
                              columns=results['columns'], lines=results['lines'])
        project.csv_data = csv_data
        project.save()
    elif file_type == "text/html":
        t_start = time.time()
        results = extract_html_data(
            upload_file, extract_tables=tables, extract_paragraphs=paragraphs)
        t_end = time.time()
        exec_time = t_end-t_start
        tables_data = []
        for table in results['tables']:
            table_file = {
                'path': table['filename'], 'filename': table['filename'], 'file_type': 'html'}
            csv_data = CsvProject(
                columns=table['columns'], lines=table['lines'], filename=table_file)
            tables_data.append(csv_data)
        html_data = HtmlProject(tables=tables_data)
        project.html_data = html_data
        project.save()
        resp = {'results': results, 'filename': filename,
                'type': 'html', 'size': file.size, "extract_tables": tables,
                "extract_paragraphs": paragraphs, 'project_id': project_id, 'execution_time': exec_time}
    elif file_type == "application/pdf":
        t_start = time.time()
        results = extract_pdf_data(
            upload_file, extract_tables=tables, extract_paragraphs=paragraphs)
        t_end = time.time()
        exec_time = t_end-t_start
        tables_data = []
        for table in results['tables']:
            table_file = {
                'path': table['filename'], 'filename': table['filename'], 'file_type': 'csv'}
            csv_data = CsvProject(
                columns=table['columns'], lines=table['lines'], filename=table_file)
            tables_data.append(csv_data)
        html_data = HtmlProject(tables=tables_data)
        project.html_data = html_data
        project.save()
        resp = {'results': results, 'filename': filename,
                'type': 'pdf', 'size': file.size, "extract_tables": tables,
                "extract_paragraphs": paragraphs, 'project_id': project_id, 'execution_time': exec_time}

    elif file_type in ['image/png', 'image/jpeg', 'image/jpg']:
        t_start = time.time()
        results = extract_image_data(
            upload_file, extract_tables=tables, extract_paragraphs=paragraphs)
        t_end = time.time()
        exec_time = t_end-t_start
        tables_data = []
        for table in results['tables']:
            table_file = {
                'path': table['filename'], 'filename': table['filename'], 'file_type': 'csv'}
            csv_data = CsvProject(
                columns=table['columns'], lines=table['lines'], filename=table_file)
            tables_data.append(csv_data)
        html_data = HtmlProject(tables=tables_data)
        project.html_data = html_data
        project.save()
        resp = {'results': results, 'filename': filename,
                'type': 'image', 'size': file.size, "extract_tables": tables,
                "extract_paragraphs": paragraphs, 'project_id': project_id, 'execution_time': exec_time}

    elif file_type == "text/plain":
        t_start = time.time()
        results = extract_text_data(upload_file)
        t_end = time.time()
        exec_time = t_end-t_start
        resp = {'results': results, 'filename': filename,
                'type': 'text', 'size': file.size, 'project_id': project_id, 'execution_time': exec_time}
    else:
        pass

    return Response(resp)


@ api_view(['POST'])
def preprocess(request):
    file_type = request.POST.get('file_type')
    project_id = request.POST.get('project_id')
    project = Project.objects.get(pk=project_id)

    if file_type == "csv":
        columns_selected = json.loads(request.POST.get('columns', 'nthg'))
        t_start = time.time()
        headers = preprocess_columns(columns_selected)
        t_end = time.time()
        exec_time = t_end-t_start
        update_csv_project(project, headers=headers)
        resp = {'columns_selected': columns_selected,
                "headers": headers, 'execution_time': exec_time}
    elif file_type == 'html':
        tables_selected = json.loads(request.POST.get('tables', 'nthg'))
        paragrahps_selected = json.loads(
            request.POST.get('paragraphs', 'nthg'))
        t_start = time.time()
        for table in tables_selected:
            if (table['selected'] == True):
                table['headers'] = preprocess_columns(table['headers'])
        for id, paragraph in enumerate(paragrahps_selected):
            if paragraph['selected'] == True:
                paragraph = preprocess_paragraph(project,
                                                 paragraph, id=id)
        t_end = time.time()
        exec_time = t_end - t_start
        update_project_tables(project, tables=tables_selected)
        update_project_paragraphs(
            project, paragraphs=paragrahps_selected)
        resp = {'tables_selected': tables_selected,
                'paragraphs_selected': paragrahps_selected, 'execution_time': exec_time}
    elif file_type == "text":
        paragraph = json.loads(request.POST.get('paragraph', 'nthg'))
        t_start = time.time()
        paragraph = preprocess_paragraph(project, paragraph)
        t_end = time.time()
        exec_time = t_end-t_start
        resp = {"data": paragraph, 'execution_time': exec_time}
    elif file_type in ['pdf', 'image']:
        tables_selected = json.loads(request.POST.get('tables', 'nthg'))
        paragrahps_selected = json.loads(
            request.POST.get('paragraphs', 'nthg'))
        t_start = time.time()
        for table in tables_selected:
            if (table['selected'] == True):
                table['headers'] = preprocess_columns(table['headers'])
        for id, paragraph in enumerate(paragrahps_selected):
            if paragraph['selected'] == True:
                paragraph = preprocess_paragraph(project,
                                                 paragraph, id=id)
        t_end = time.time()
        exec_time = t_end - t_start
        update_project_tables(project, tables=tables_selected)
        update_project_paragraphs(
            project, paragraphs=paragrahps_selected)
        resp = {'tables_selected': tables_selected,
                'paragraphs_selected': paragrahps_selected, 'execution_time': exec_time}

    return Response(resp)


@ api_view(['GET'])
def select_vocabs(request):
    vocabs = get_vocab_list()
    results = VocabularySerializer(vocabs, many=True).data
    return Response(results)


@ api_view(['POST'])
def explore(request):
    file_type = request.POST.get("file_type")
    list_vocabs = []
    project_id = request.POST.get("project_id")
    vocabs = json.loads(request.POST.get("vocabs"))
    project_vocabs = []
    project = Project.objects.get(pk=project_id)
    for v in vocabs:
        vocab = Vocabulary(prefix=v['prefix'], uri=v["uri"], title=v['title'])
        project_vocabs.append(vocab)
        list_vocabs.append(v["prefix"])
    project.vocabularies = project_vocabs
    project.save()
    if file_type == "csv":
        cols = json.loads(request.POST.get('columns'))
        terms = []
        t_start = time.time()
        for col in cols:
            if col['selected'] == True:
                terms.append(explore_column(col, list_vocabs))
        t_end = time.time()
        exec_time = t_end-t_start
        resp = {"terms": terms, 'execution_time': exec_time}
        return Response(resp)
    elif file_type in ["html", 'pdf', 'image']:
        tables = json.loads(request.POST.get('tables'))
        paragraphs = json.loads(request.POST.get('paragraphs'))
        t_start = time.time()
        for table in tables:
            if table['selected'] == True:
                table['terms'] = []
                for header in table['headers']:
                    if header["selected"] == True:
                        table['terms'].append(
                            explore_column(header, list_vocabs))
        for paragraph in paragraphs:
            if paragraph['selected']:
                paragraph = explore_paragraph(paragraph, list_vocabs)
        t_end = time.time()
        exec_time = t_end-t_start
        return Response({"tables": tables, "paragraphs": paragraphs, 'execution_time': exec_time})

    elif file_type == "text":
        paragraph = json.loads(request.POST.get('paragraph'))
        t_start = time.time()
        paragraph = explore_paragraph(paragraph, list_vocabs)
        t_end = time.time()
        exec_time = t_end-t_start
        return Response({"data": paragraph, 'execution_time': exec_time})


@ api_view(['POST'])
def convert(request):
    file_type = request.POST.get("file_type")
    file_name = request.POST.get("file_name")
    project_id = request.POST.get("project_id")
    project = Project.objects.get(pk=project_id)
    if file_type == "csv":
        terms = json.loads(request.POST.get("terms"))
        row_class = json.loads(request.POST.get("rowClass"))
        headers_id = json.loads(request.POST.get("headersId"))
        if headers_id:
            project.csv_data.headers_id = [
                Header(name=header) for header in headers_id]
            project.save()
        for term in terms:
            headers = project.csv_data.headers
            for head in headers:
                if head.name == term['property']:
                    if term["term"]["uri"]:
                        head.term = term["term"]["uri"]
            project.save()
        delimiter = request.POST.get("delimiter")
        t_start = time.time()
        lines = convert_csv(project, file_name, delimiter,
                            terms, headers_id, row_class)
        t_end = time.time()
        exec_time = t_end-t_start
        #update_csv_project(project, triplets=lines)
        return Response({"data": lines, 'execution_time': exec_time})
    if file_type == "text":
        terms = json.loads(request.POST.get("terms"))
        triplets = json.loads(request.POST.get("triplets"))
        entities = json.loads(request.POST.get("entities"))
        t_start = time.time()
        lines = convert_text(triplets, terms, entities, project)
        t_end = time.time()
        exec_time = t_end-t_start
        update_text_project(project, terms=lines, triplets=triplets)
        return Response({"data": lines, 'execution_time': exec_time})
    if file_type in ["html", 'pdf', 'image']:
        tables = json.loads(request.POST.get("tables"))
        paragraphs = json.loads(request.POST.get("paragraphs"))
        tables_triplets = []
        paragraphs_triplets = []
        t_start = time.time()
        for table in tables:
            line = dict()
            line["id"] = table['id']
            line['triplets'] = convert_html(table, project)
            tables_triplets.append(line)
            update_project_tables(
                project, triplets=tables_triplets, headers=tables)
        for id, paragraph in enumerate(paragraphs):
            triplets = paragraph['triplets']
            terms = paragraph['terms']
            entities = paragraph['entities']
            line = dict()
            line['id'] = paragraph["id"]
            line["triplets"] = convert_text(
                triplets, terms, entities, project, id)
            paragraphs_triplets.append(line)
            update_project_paragraphs(project, terms=paragraphs_triplets)
        t_end = time.time()
        exec_time = t_end-t_start
        return Response({"tables": tables_triplets,
                         'paragraphs': paragraphs_triplets,
                         'execution_time': exec_time})


@ api_view(["POST"])
def document(request):
    project_id = request.POST.get("project_id")
    metadata = json.loads(request.POST.get("metadata"))
    format = request.POST.get("format")
    project = Project.objects.get(pk=project_id)
    document_project(project, metadata, format)
    project = Project.objects.get(pk=project_id)
    project_serializer = ProjectSerializer(project)
    return Response({'success': "success", "project": project_serializer.data})


@api_view(["POST"])
def rdf_translate(request):
    format = request.POST.get("format")
    project_id = request.POST.get("project_id")
    project = Project.objects.get(pk=project_id)
    translate_file(project, format)
    return Response({"msg": "success"})


@ api_view(['POST'])
def search_property(request):
    term = request.POST.get("term")
    vocab_list = get_vocab(term)
    return Response(vocab_list)


@ api_view(['POST'])
def search_class(request):
    term = request.POST.get("term")
    vocab_list = get_vocab(term, term_type="class")
    return Response(vocab_list)


@ api_view(['POST'])
def create_property(request):
    prop = json.loads(request.POST.get("prop"))
    project_id = request.POST.get("project_id")
    project = Project.objects.get(pk=project_id)
    property_serializer = PropertySerializer(data=prop)
    if property_serializer.is_valid():
        properiety = Propriety(
            label=prop["label"], comment=prop["comment"], subPropertyOf=prop['subPropertyOf'])
        if project.properties == None:
            project.properties = [properiety]
        else:
            project.properties.append(properiety)
        project.save()
    else:
        return Response({"msg": property_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    prop = {'term': properiety.label,
            "prefixedName": "dataset:"+properiety.label, 'uri': "dataset:"+properiety.label}
    return Response(prop)


@ api_view(['POST'])
def create_class(request):
    rdf_class = json.loads(request.POST.get("class"))
    project_id = request.POST.get("project_id")
    project = Project.objects.get(pk=project_id)
    class_serializer = ClassSerializer(data=rdf_class)
    if class_serializer.is_valid():
        new_class = RdfClass(
            label=rdf_class["label"], comment=rdf_class["comment"], subClassOf=rdf_class['subClassOf'])
        project.csv_data.row_class = new_class
        project.save()
    else:
        return Response({"msg": class_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    prop = {'term': new_class.label,
            "prefixedName": "dataset:"+new_class.label, "class": rdf_class}
    return Response(prop)


@ api_view(["POST"])
def register(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    password = data.get("password")
    user = MyUser.objects.create_user(
        email=email, first_name=first_name, last_name=last_name, password=password)

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return Response({"token": token, "email": user.email, "id": user.id, "last_name": user.last_name, "first_name": first_name})
