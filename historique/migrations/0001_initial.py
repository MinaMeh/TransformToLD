# Generated by Django 2.2.12 on 2020-06-06 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='inputOpenData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('file', models.FileField(upload_to='')),
                ('link', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=500)),
                ('addition_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='', max_length=70)),
                ('description', models.CharField(default='', max_length=400)),
                ('licence', models.CharField(default='', max_length=100)),
                ('author', models.CharField(default='', max_length=50)),
                ('updated', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('inputFile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historique.inputOpenData')),
            ],
        ),
    ]