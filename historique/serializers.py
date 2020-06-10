
from rest_meets_djongo import serializers
from historique.models import Project, Author


class AuthorSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'email', 'password')


class ProjectSerializer(serializers.DjongoModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'project_name',
            'description',
            'licence',
            'author',
            'creation_date',
            'file_path'
        )
