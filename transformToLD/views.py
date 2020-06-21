from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from transformToLD.Helpers.extract import extract_text_data, extract_csv_data, extract_html_data
from transformToLD.Helpers.explore import get_vocab_list, explore_csv, explore_column, get_vocab, explore_paragraph
from transformToLD.Helpers.preprocess import preprocess_columns, preprocess_paragraph
from transformToLD.Helpers.convert import convert_csv, convert_text, convert_html
import pandas as pd
import csv
import json
import io
from rest_framework import viewsets, static
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .Serializers import VocabularySerializer, ProjectSerializer
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from transformToLD.models import Project
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from transformToLD.models import MyUser
# Create your views here.
from rest_framework_jwt.settings import api_settings
from historique.models import Project
from historique.serializers import ProjectSerializer


@api_view(['GET'])
def test(request):
    # Project.objects.all().delete()
    # test = Project(project_name="test5", file_path="test/test").save()
    test2 = Project.objects.all()
    # pr = ProjectSerializer(test2).data
    ser = ProjectSerializer(test2, many=True).data
    return Response(ser)


@api_view(['GET'])
def listVocabs(request):
    vocabs = get_vocab_list()
    results = VocabularySerializer(vocabs, many=True).data
    return Response(results)


@api_view(['POST'])
def extract(request):
    file = request.FILES['file']
    project_name = request.POST.get('project_name')
    separator = request.POST.get('separator')
    project = json.loads(request.POST.get("project"))

    project_serializer = ProjectSerializer(data=project)

    if project_serializer.is_valid():
        project_serializer.save()
    else:
        return Response(project_serializer.data)
    tables = True if request.POST.get('tables') == 'true' else False
    paragraphs = True if request.POST.get('paragraphs') == 'true' else False
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    upload_file = fs.url(filename)
    file_type = file.content_type
    # Project(project_name=project_name, file_path=upload_file).save()
    if file_type == 'text/csv' or file_type == "application/vnd.ms-excel":
        results = extract_csv_data(upload_file, separator)
        resp = {'results': results, 'filename': filename,
                'type': 'csv', 'size': file.size}
    elif file_type == "text/html":
        results = extract_html_data(
            upload_file, extract_tables=tables, extract_paragraphs=paragraphs)
        resp = {'results': results, 'filename': filename,
                'type': 'html', 'size': file.size, "extract_tables": tables, "extract_paragraphs": paragraphs}
    elif file_type == "text/plain":
        results = extract_text_data(upload_file)
        resp = {'results': results, 'filename': filename,
                'type': 'text', 'size': file.size}
    else:
        pass

    return Response(resp)


@api_view(['POST'])
def preprocess(request):
    file_type = request.POST.get('file_type')
    if file_type == "csv":
        columns_selected = json.loads(request.POST.get('columns', 'nthg'))
        headers = preprocess_columns(columns_selected)
        resp = {'columns_selected': columns_selected, "headers": headers}
    elif file_type == 'html':
        tables_selected = json.loads(request.POST.get('tables', 'nthg'))
        paragrahps_selected = json.loads(
            request.POST.get('paragraphs', 'nthg'))
        for table in tables_selected:
            if (table['selected'] == True):
                table['headers'] = preprocess_columns(table['headers'])
        for paragraph in paragrahps_selected:
            if paragraph['selected'] == True:
                paragraph = preprocess_paragraph(
                    paragraph)
        resp = {'tables_selected': tables_selected,
                'paragraphs_selected': paragrahps_selected}
    elif file_type == "text":
        paragraph = json.loads(request.POST.get('paragraph', 'nthg'))
        paragraph = preprocess_paragraph(paragraph)
        resp = paragraph
    return Response(resp)


@api_view(['GET'])
def select_vocabs(request):
    vocabs = get_vocab_list()
    results = VocabularySerializer(vocabs, many=True).data
    return Response(results)


@api_view(['POST'])
def explore(request):
    file_type = request.POST.get("file_type")
    list_vocabs = json.loads(request.POST.get("vocabs"))
    if file_type == "csv":
        cols = json.loads(request.POST.get('columns'))
        terms = []
        for col in cols:
            if col['selected'] == True:
                terms.append(explore_column(col, list_vocabs))
        resp = {"terms": terms}
        return Response(resp)
    elif file_type == "html":
        tables = json.loads(request.POST.get('tables'))
        paragraphs = json.loads(request.POST.get('paragraphs'))
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
        return Response({"tables": tables, "paragraphs": paragraphs})
    elif file_type == "text":
        paragraph = json.loads(request.POST.get('paragraph'))
        paragraph = explore_paragraph(paragraph, list_vocabs)
        return Response(paragraph)


@api_view(['POST'])
def convert(request):
    file_type = request.POST.get("file_type")
    file_name = request.POST.get("file_name")
    if file_type == "csv":
        terms = json.loads(request.POST.get("terms"))
        delimiter = request.POST.get("delimiter")
        lines = convert_csv(file_name, delimiter, terms)
        return Response(lines)
    if file_type == "text":
        terms = json.loads(request.POST.get("terms"))
        triplets = json.loads(request.POST.get("triplets"))
        lines = convert_text(triplets, terms)
        return Response(lines)
    if file_type == "html":
        tables = json.loads(request.POST.get("tables"))
        paragraphs = json.loads(request.POST.get("paragraphs"))
        tables_triplets = []
        paragraphs_triplets = []
        for table in tables:
            line = dict()
            line["id"] = table['id']
            line['triplets'] = convert_html(table)
            tables_triplets.append(line)
        for paragraph in paragraphs:
            triplets = paragraph['triplets']
            terms = paragraph['terms']
            line = dict()
            line['id'] = paragraph["id"]
            line["triplets"] = convert_text(triplets, terms)
            paragraphs_triplets.append(line)

        return Response({"tables": tables_triplets, 'paragraphs': paragraphs_triplets})


@api_view(['POST'])
def search_property(request):
    term = request.POST.get("term")
    vocab_list = get_vocab(term)
    return Response(vocab_list)


@api_view(["POST"])
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
