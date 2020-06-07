from djongo import models
from django import forms


class Author(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField()

    class Meta:
        abstract = True

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'name', 'email'
        )

class Project(models.Model):
    project_name = models.CharField(max_length=70, blank=False, default='')
    description = models.TextField()
    licence = models.CharField(max_length=100, blank=False, default='')
    author = models.EmbeddedField(
        model_container=Author,
        model_form_class=AuthorForm,
        null=False
    )
    updated = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    file_path = models.TextField()
    objects = models.DjongoManager()

    def __str__(self):
        return "%s" % (self.project_name)
