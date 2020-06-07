from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from historique.models import Project, Author
from historique.serializers import ProjectSerializer, AuthorSerializer

from rest_framework.decorators import api_view


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


'''
@api_view(['GET'])
def project_list_updated(request):
    projects = Project.objects.filter(updated=True)

    if request.method == 'GET':
        projects_serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(projects_serializer.data, safe=False)
'''
