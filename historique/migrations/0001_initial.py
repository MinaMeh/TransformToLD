# Generated by Django 2.2.12 on 2020-06-23 15:23

from django.db import migrations, models
import djongo.models.fields
import historique.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='CsvProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('separator', models.CharField(max_length=3)),
                ('lines', models.IntegerField()),
                ('columns', models.IntegerField()),
                ('headers', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Header, null=True)),
                ('triplets', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Triplet, null=True)),
                ('table_file', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('filename', models.CharField(max_length=100)),
                ('file_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.CharField(max_length=50)),
                ('term', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='', max_length=70, unique=True)),
                ('description', models.TextField(null=True)),
                ('vocabularies', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Vocabulary, null=True)),
                ('licence', models.CharField(default='', max_length=100, null=True)),
                ('author', djongo.models.fields.EmbeddedField(model_container=historique.models.Author, model_form_class=historique.models.AuthorForm, null=True)),
                ('input_file', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
                ('csv_data', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.CsvProject, null=True)),
                ('text_data', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.TextProject, null=True)),
                ('html_data', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.HtmlProject, null=True)),
                ('output_files', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.File, null=True)),
                ('intermediate_files', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.File, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('triplets', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Triplet, null=True)),
                ('terms', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Header, null=True)),
                ('p_file', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Triplet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_subject', models.CharField(max_length=255)),
                ('t_predicate', models.CharField(max_length=255)),
                ('t_object', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=10)),
                ('uri', models.CharField(max_length=255)),
            ],
        ),
    ]
