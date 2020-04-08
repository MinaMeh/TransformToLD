from rest_framework import serializers

class VocabularySerializer(serializers.Serializer):
    prefix= serializers.CharField(max_length=250)
    uri= serializers.CharField(max_length=250)
    title= serializers.CharField(max_length=250)