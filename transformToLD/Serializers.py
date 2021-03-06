from rest_framework import serializers


class VocabularySerializer(serializers.Serializer):
    prefix = serializers.CharField(max_length=250)
    uri = serializers.CharField(max_length=250)
    title = serializers.CharField(max_length=250)


class ProjectSerializer(serializers.Serializer):
    project_name = serializers.CharField(max_length=30)
    file_path = serializers.URLField()
