# Generated by Django 2.2.12 on 2020-07-21 22:56

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
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('separator', models.CharField(blank=True, max_length=3, null=True)),
                ('lines', models.IntegerField()),
                ('columns', models.IntegerField()),
                ('headers', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Header, null=True)),
                ('triplets', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
                ('filename', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
                ('headers_id', djongo.models.fields.ArrayField(blank=True, default=[], model_container=historique.models.Header, null=True)),
                ('row_class', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.RdfClass, null=True)),
                ('selected', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('term', models.CharField(blank=True, max_length=255, null=True)),
                ('combinaison', djongo.models.fields.ListField(blank=True, default=[], null=True)),
                ('translated', models.CharField(blank=True, max_length=50, null=True)),
                ('selected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HtmlProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tables', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.CsvProject, null=True)),
                ('paragraphs', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.TextProject, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(max_length=255)),
                ('createdAt', models.DateField()),
                ('subject', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('license', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='', max_length=255)),
                ('user_id', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('vocabularies', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Vocabulary, null=True)),
                ('licence', models.CharField(default='', max_length=255, null=True)),
                ('author', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.Author, model_form_class=historique.models.AuthorForm, null=True)),
                ('input_file', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
                ('csv_data', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.CsvProject, null=True)),
                ('text_data', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.TextProject, null=True)),
                ('html_data', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.HtmlProject, null=True)),
                ('output_files', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.File, null=True)),
                ('intermediate_files', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.File, null=True)),
                ('properties', djongo.models.fields.ArrayField(blank=True, model_container=historique.models.Propriety, null=True)),
                ('metadata', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.MetaData, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('converted', models.BooleanField(default=False)),
                ('converted_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Propriety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
                ('comment', models.TextField()),
                ('subPropertyOf', models.TextField(blank=True, null=True)),
                ('uri', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RdfClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
                ('comment', models.TextField()),
                ('subClassOf', models.TextField(blank=True, null=True)),
                ('uri', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TextProject',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('triplets', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
                ('terms', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
                ('p_file', djongo.models.fields.EmbeddedField(blank=True, model_container=historique.models.File, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Triplet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('predicate', models.CharField(max_length=255)),
                ('object', models.CharField(max_length=255)),
                ('object_type', models.CharField(max_length=20)),
                ('selected', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=10)),
                ('uri', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
    ]
