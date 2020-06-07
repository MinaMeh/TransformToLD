from rest_framework import serializers
from historique.models import Project, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'email', 'password')

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        author = Author.objects.update(**validated_data)
        return author


class ProjectSerializer(serializers.ModelSerializer):

    file_path = serializers.URLField()
    author = AuthorSerializer(required=True, read_only=False)

    class Meta:
        model = Project
        fields = (
            'project_name',
            'description',
            'licence',
            'author',
            'updated',
            'creation_date',
            'file_path'
        )

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        if author_data:
            author = Author.objects.get_or_create(**author_data)[0]
            validated_data['author'] = author
        return Project.objects.create(**validated_data)
