
from rest_meets_djongo import serializers
from historique.models import Project, Author, File


class AuthorSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'email', 'password')


class FileSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = File
        fields = ('path', 'filename', 'file_type')


class ProjectSerializer(serializers.DjongoModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'project_name',
            'description',
            'licence',
            'author',
            'input_file',
            'output_files',
            'intermediate_files',
            'csv_data',
            'text_data',
            'html_data',
            'creation_date',
            'converted',
            'vocabularies',
            'user_id'
        )
