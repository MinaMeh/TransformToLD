from djongo import models
from django import forms


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
    file_type = models.CharField(max_length=10)


class Triplet(models.Model):
    t_subject = models.CharField(max_length=255)
    t_predicate = models.CharField(max_length=255)
    t_object = models.CharField(max_length=255)


class Header(models.Model):
    column = models.CharField(max_length=50)
    term = models.CharField(max_length=255)


class Vocabulary(models.Model):
    prefix = models.CharField(max_length=10)
    uri = models.CharField(max_length=255)


class CsvProject(models.Model):
    separator = models.CharField(max_length=3)
    lines = models.IntegerField()
    columns = models.IntegerField()
    headers = models.ArrayField(model_container=Header, null=True, blank=True)
    triplet = models.ArrayField(model_container=Triplet, null=True, blank=True)
    table_file = models.EmbeddedField(
        model_container=File, null=True, blank=True)


class TextProject(models.Model):
    triplets = models.ArrayField(
        model_container=Triplet, null=True, blank=True)
    terms = models.ArrayField(model_container=Header, null=True, blank=True)
    p_file = models.EmbeddedField(model_container=File, null=True, blank=True)


class HtmlProject():
    tables = models.ArrayField(
        model_container=CsvProject, null=True, blank=True)
    paragraphs = models.ArrayField(
        model_container=TextProject, null=True, blank=True)


class Project(models.Model):
    project_name = models.CharField(max_length=70, blank=False, default='')
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
    csv_data = models.ArrayField(
        model_container=CsvProject, null=True, blank=True)
    text_data = models.ArrayField(
        model_container=TextProject, null=True, blank=True)
    html_data = models.ArrayField(
        model_container=HtmlProject, null=True, blank=True)
    output_files = models.ArrayField(
        model_container=File, null=True, blank=True)
    intermediate_files = models.ArrayField(
        model_container=File, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.DjongoManager()
