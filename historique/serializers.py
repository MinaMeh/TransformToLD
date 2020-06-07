from rest_framework import serializers
from historique.models import Project, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'name', 'email'
        ]


class ProjectSerializer(serializers.ModelSerializer):

    file_path = serializers.URLField()
    author = AuthorSerializer()

    class Meta:
        model = Project
        fields = [
            'project_name',
            'description',
            'licence',
            'author',
            'updated',
            'creation_date',
            'file_path'
        ]
