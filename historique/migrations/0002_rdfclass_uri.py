# Generated by Django 2.2.12 on 2020-07-06 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historique', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rdfclass',
            name='uri',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]