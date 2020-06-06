from rest_framework import serializers
from historique.models import Project, inputOpenData


class inputOpenDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = inputOpenData
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `input Open Data` instance, given the validated data.
        """
        return inputOpenData.objects.create(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):

    inputOpenDataFile = inputOpenDataSerializer(required=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):

        inputOpenDataFile_data = validated_data.pop('inputOpenDataFile')
        inputOpenDataFile = inputOpenData.objects.create(
            **inputOpenDataFile_data)

        project = Project.objects.create(
            inputOpenDataFile=inputOpenDataFile, **validated_data)
        return project

    def update(self, instance, validated_data):
        project = Project.objects.update(**validated_data)
        return project


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['updated']
