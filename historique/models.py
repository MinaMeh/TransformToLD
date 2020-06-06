from django.db import models


class Project(models.Model):
    project_name = models.CharField(max_length=70, blank=False, default='')
    description = models.TextField()
    licence = models.CharField(max_length=100, blank=False, default='')
    author = models.CharField(max_length=50, blank=False, default='')
    updated = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.project_name)


class inputOpenData(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')
    file = models.FileField()
    link = models.CharField(max_length=200, blank=False, default='')
    description = models.TextField()
    addition_date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s" % (self.name)

