from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from historique.models import Project, inputOpenData
from historique.serializers import ProjectSerializer, inputOpenDataSerializer
