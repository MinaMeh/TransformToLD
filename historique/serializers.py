from rest_framework import serializers
from historique.models import Project, inputOpenData


class inputOpenDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = inputOpenData
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    #inputOpenDataFile = inputOpenDataSerializer(required=True)

    class Meta:
        model = Project
        fields = '__all__'
