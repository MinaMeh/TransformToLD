from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from historique.models import Project, Author
from historique.serializers import ProjectSerializer, AuthorSerializer


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def projects_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        email = request.GET.get('user_email', None)
        projects = projects.filter(
            author={'email': email})
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
