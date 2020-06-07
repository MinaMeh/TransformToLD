# Generated by Django 2.2.12 on 2020-06-07 11:04

from django.db import migrations, models
import djongo.models.fields
import historique.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='', max_length=70)),
                ('description', models.TextField()),
                ('licence', models.CharField(default='', max_length=100)),
                ('author', djongo.models.fields.EmbeddedField(model_container=historique.models.Author, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('file_path', models.TextField()),
            ],
        ),
    ]
