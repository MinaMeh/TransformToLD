import shutil
from django.conf import settings
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from historique.models import Project, Author, Header
from historique.serializers import ProjectSerializer, AuthorSerializer
import csv
from transformToLD.Controllers.explore import get_vocab_list
from transformToLD.Serializers import VocabularySerializer


@api_view(['POST'])
def test(request):
    header = JSONParser().parse(request)
    Header.objects.create(**header)
    return Response(header)


@api_view(['GET', 'POST', 'DELETE'])
# @permission_classes((IsAuthenticated,))
def projects_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        user_id = request.GET.get('user_id', None)
        projects = projects.filter(
            user_id=user_id)
        projects_serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(projects_serializer.data, safe=False)

    elif request.method == 'POST':
        project_data = JSONParser().parse(request)
        project_serializer = ProjectSerializer(data=project_data)

        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse(project_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(project_serializer.errors)

    elif request.method == 'DELETE':
        count = Project.objects.all().delete()
        return JsonResponse({'message': '{} Projects were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def project_details(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return JsonResponse({'message': 'The project does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        triplets = []
        terms = []
        if project.csv_data:
            triplets_file = project.csv_data.triplets.path
            with open(triplets_file, 'r') as f:
                triplets_writer = csv.DictReader(f)
                for triplet in triplets_writer:
                    triplets.append(triplet)

        if project.text_data:
            triplets_file = project.text_data.triplets.path
            with open(triplets_file, 'r') as f:
                triplets_writer = csv.DictReader(f)
                for triplet in triplets_writer:
                    triplets.append(triplet)
            terms_file = project.text_data.terms.path
            with open(terms_file, 'r') as f:
                terms_reader = csv.DictReader(f)
                for term in terms_reader:
                    terms.append(term)

        if project.html_data:
            for table in project.html_data.tables:
                triplets_file = table.triplets.path
                with open(triplets_file, 'r') as f:
                    triplets_writer = csv.DictReader(f)
                    for triplet in triplets_writer:
                        triplets.append(triplet)
            for paragprah in project.html_data.paragraphs:
                triplets_file = paragprah.terms.path
                with open(triplets_file) as f:
                    triplets_writer = csv.DictReader(f)
                    for triplet in triplets_writer:
                        triplets.append(triplet)
                terms_file = paragprah.triplets.path
                with open(terms_file, 'r') as f:
                    terms_reader = csv.DictReader(f)
                    for term in terms_reader:
                        terms.append(term)

        vocabs = get_vocab_list()
        results = VocabularySerializer(vocabs, many=True).data
        project_serializer = ProjectSerializer(project)
        return Response({"project": project_serializer.data, "triplets": triplets, 'terms': terms, "vocabularies": results})

    elif request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project_serializer = ProjectSerializer(project, data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse(project_serializer.data)
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        directory = "{}{}/{}".format(settings.MEDIA_URL,
                                     project.user_id, project.project_name)
        shutil.rmtree(directory)
        project.delete()
        return JsonResponse({'message': 'Project was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
