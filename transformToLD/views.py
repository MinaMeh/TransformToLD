from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from transformToLD.Components.CSVComponent import trait_csv, read_csv
from transformToLD.Components.HTMLComponent import trait_html 
from transformToLD.Helpers.explore import get_vocab_list
import pandas as pd
import csv
import io
from rest_framework import viewsets, static
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .Serializers import VocabularySerializer
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.
@api_view(['GET'])
def listVocabs(request):
    vocabs= get_vocab_list()
    results= VocabularySerializer(vocabs,many=True).data
    return Response(results)

@api_view(['POST'])
def preprocess(request):
    file = request.FILES['file']
    fs= FileSystemStorage()
    filename= fs.save(file.name,file)
    upload_file= fs.url(filename)
    file_type = file.content_type
    if file_type == 'text/csv':
        results = read_csv(upload_file)
        resp = {'results': results, 'filename': filename, 'type': 'csv'}
    else:
        pass
    return Response(resp)

@api_view (['POST'])
def properties(request):
    file=request.FILES['file']
    fs= FileSystemStorage()
    filename= fs.save(file.name,file)
    upload_file= fs.url(filename)
    file_type= file.content_type
    if (file_type=='text/csv'):
        vocabs=request.POST['vocabs']
        results= trait_csv(upload_file,vocabs)
        resp={'results': results,'filename':filename, 'type': 'csv'}
    elif (file_type=='text/html'):
        results= trait_html(upload_file,request.POST['vocabs'])
        resp={'results':results, 'tables':0, "paragraphs":0, "type": "html",'filename':filename}
    return Response(resp)