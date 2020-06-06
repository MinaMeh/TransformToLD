from django.db import models


class inputOpenData(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')
    file = models.FileField()
    link = models.CharField(max_length=200, blank=False, default='')
    description = models.CharField(max_length=500, blank=False, default='')
    addition_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.name)


class Project(models.Model):
    project_name = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=400, blank=False, default='')
    licence = models.CharField(max_length=100, blank=False, default='')
    author = models.CharField(max_length=50, blank=False, default='')
    updated = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    inputFile = models.ForeignKey(inputOpenData, on_delete=models.CASCADE ,null=True)

    def __str__(self):
        return "%s" % (self.project_name)
