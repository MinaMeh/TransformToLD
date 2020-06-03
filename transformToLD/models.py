from djongo import models

# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=30)
    file_path = models.TextField()
    objects = models.DjongoManager()
