from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from historique.models import Project, inputOpenData
from historique.serializers import ProjectSerializer, inputOpenDataSerializer

from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def inputOpenDataList(request):
    # GET list of inputOpenData, POST a new source file, DELETE all inputs
    if request.method == 'GET':
        inputFiles = inputOpenData.objects.all()

        nameFile = request.GET.get('name', None)
        if nameFile is not None:
            inputFiles = inputFiles.filter(title__icontains=nameFile)

        inputFiles_serializer = InputOpenDataSerializer(inputFiles, many=True)
        return JsonResponse(inputFiles_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        inputFile_data = JSONParser().parse(request)
        inputFile_serializer = InputOpenDataSerializer(data=inputFile_data)
        if inputFile_serializer.is_valid():
            inputFile_serializer.save()
            return JsonResponse(inputFile_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(inputFile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = inputOpenData.objects.all().delete()
        return JsonResponse({'message': '{} Datasets were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
def projects_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()

        project_name = request.GET.get('project_name', None)
        if project_name is not None:
            projects = projects.filter(project_name__icontains=project_name)

        projects_serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(projects_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        project_data = JSONParser().parse(request)
        project_serializer = ProjectSerializer(data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse(project_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Project.objects.all().delete()
        return JsonResponse({'message': '{} Projects were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def inputOpenData_details(request, pk):
    try:
        inputFile = inputOpenData.objects.get(pk=pk)
    except inputOpenData.DoesNotExist:
        return JsonResponse({'message': 'The input open data does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        inputFile_serializer = InputOpenDataSerializer(inputFile)
        return JsonResponse(inputFile_serializer.data)

    elif request.method == 'PUT':
        inputFile_data = JSONParser().parse(request)
        inputFile_serializer = InputOpenDataSerializer(
            inputFile, data=inputFile_data)
        if inputFile_serializer.is_valid():
            inputFile_serializer.save()
            return JsonResponse(inputFile_serializer.data)
        return JsonResponse(inputFile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        inputFile.delete()
        return JsonResponse({'message': 'input open data was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def project_details(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return JsonResponse({'message': 'The project does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        project_serializer = ProjectSerializer(project)
        return JsonResponse(project_serializer.data)

    elif request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project_serializer = ProjectSerializer(project, data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse(project_serializer.data)
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return JsonResponse({'message': 'Project was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
