from rest_framework import serializers
from historique.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    
    file_path = serializers.URLField()

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
