from djongo import models
from django import forms

class inputOpenData(models.Model):
    file = models.FileField()
    link = models.URLField(max_length=200, blank=False, default='')
    addition_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%d" % (self.pk)

    class Meta:
        abstract = True


class inputOpenDataForm(forms.ModelForm):
    class Meta:
        model = inputOpenData
        fields = [
            'file', 'link'
        ]


class Project(models.Model):
    project_name = models.CharField(max_length=70, blank=False, default='')
    description = models.TextField()
    licence = models.CharField(max_length=100, blank=False, default='')
    author = models.CharField(max_length=50, blank=False, default='')
    updated = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    inputFile = models.EmbeddedField(
        model_container=inputOpenData,
        model_form_class=inputOpenDataForm,
        null=False
    )
    objects = models.DjongoManager()

    def __str__(self):
        return "%s" % (self.project_name)
