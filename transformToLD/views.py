from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from transformToLD.Helpers.extract import extract_text_data, extract_csv_data, extract_html_data
from transformToLD.Helpers.explore import get_vocab_list, explore_csv, explore_column, get_vocab
from transformToLD.Helpers.preprocess import preprocess_columns, preprocess_paragraph
import pandas as pd
import csv
import json
import io
from rest_framework import viewsets, static
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .Serializers import VocabularySerializer, ProjectSerializer
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from transformToLD.models import Project
from rest_framework import serializers

# Create your views here.


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
    tables = True if request.POST.get('tables') == 'true' else False
    paragraphs = True if request.POST.get('paragraphs') == 'true' else False
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    upload_file = fs.url(filename)
    file_type = file.content_type
    # Project(project_name=project_name, file_path=upload_file).save()
    if file_type == 'text/csv':
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
    else:
        resp = {'file_type': request}
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
    if file_type == "text":
        pass


@ api_view(['POST'])
def properties(request):
    file = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    upload_file = fs.url(filename)
    file_type = file.content_type
    if (file_type == 'text/csv'):
        vocabs = request.POST['vocabs']
        results = trait_csv(upload_file, vocabs)
        resp = {'results': results, 'filename': filename, 'type': 'csv'}
    elif (file_type == 'text/html'):
        results = trait_html(upload_file, request.POST['vocabs'])
        resp = {'results': results, 'tables': 0, "paragraphs": 0,
                "type": "html", 'filename': filename}
    return Response(resp)


@api_view(['POST'])
def search_property(request):
    term = request.POST.get("term")
    vocab_list = get_vocab(term)
    return Response(vocab_list)
