# Generated by Django 2.2.12 on 2020-06-28 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historique', '0003_project_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]