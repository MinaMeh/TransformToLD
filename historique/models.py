from djongo import models
from django import forms


class Author(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return "%s" % (self.name)
    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data.
        """
        return Author.objects.create(**validated_data)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'name', 'email', 'password'
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
    file_path = models.TextField(default='')
    updated = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True) 
    objects = models.DjongoManager()

    def __str__(self):
        return "%d,%s" % (self.pk, self.project_name)
