from djongo import models
from django import forms
from django.contrib.postgres.fields import ArrayField


class Author(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField()

    def __str__(self):
        return "%s" % (self.email)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Author.objects.create(**validated_data)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'first_name', 'last_name', 'email'
        )


class File(models.Model):
    path = models.TextField()
    filename = models.CharField(max_length=100)
    file_type = models.CharField(max_length=50)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return File.objects.create(**validated_data)


class Triplet(models.Model):
    subject = models.CharField(max_length=255)
    predicate = models.CharField(max_length=255)
    object = models.CharField(max_length=255)
    selected = models.BooleanField(default=True)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Triplet.objects.create(**validated_data)


class Header(models.Model):
    name = models.CharField(max_length=50)
    term = models.CharField(max_length=255, null=True, blank=True)
    combinaison = models.ListField(null=True, blank=True, default=[])
    translated = models.CharField(max_length=20, null=True, blank=True)
    selected = models.BooleanField(default=False)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Header.objects.create(**validated_data)


class Vocabulary(models.Model):
    prefix = models.CharField(max_length=10)
    uri = models.CharField(max_length=255)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Vocabulary.objects.create(**validated_data)


class CsvProject(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    separator = models.CharField(max_length=3, null=True, blank=True)
    lines = models.IntegerField()
    columns = models.IntegerField()
    headers = models.ArrayField(model_container=Header, null=True, blank=True)
    triplets = models.ArrayField(
        model_container=Triplet, null=True, blank=True)
    filename = models.EmbeddedField(
        model_container=File, null=True, blank=True)
    selected = models.BooleanField(null=True,  blank=True, default=False)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return CsvProject.objects.create(**validated_data)


class TextProject(models.Model):
    triplets = models.ArrayField(
        model_container=Triplet, null=True, blank=True)
    terms = models.ArrayField(model_container=Header, null=True, blank=True)
    p_file = models.EmbeddedField(model_container=File, null=True, blank=True)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return TextProject.objects.create(**validated_data)


class HtmlProject(models.Model):
    tables = models.ArrayField(
        model_container=CsvProject, null=True, blank=True)
    paragraphs = models.ArrayField(
        model_container=TextProject, null=True, blank=True)

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return HtmlProject.objects.create(**validated_data)


class Project(models.Model):
    project_name = models.CharField(
        max_length=70, blank=False, default='', unique=True)
    description = models.TextField(null=True)
    vocabularies = models.ArrayField(
        model_container=Vocabulary, null=True, blank=True)
    licence = models.CharField(
        max_length=100, blank=False, null=True, default='')
    author = models.EmbeddedField(
        model_container=Author,
        model_form_class=AuthorForm,
        null=False
    )
    input_file = models.EmbeddedField(
        model_container=File,
        null=True,
        blank=True

    )
    csv_data = models.EmbeddedField(
        model_container=CsvProject, null=True, blank=True)
    text_data = models.EmbeddedField(
        model_container=TextProject, null=True, blank=True)
    html_data = models.EmbeddedField(
        model_container=HtmlProject, null=True, blank=True)
    output_files = models.ArrayField(
        model_container=File, null=True, blank=True)
    intermediate_files = models.ArrayField(
        model_container=File, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(auto_now=False)
    objects = models.DjongoManager()

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Project.objects.create(**validated_data)
