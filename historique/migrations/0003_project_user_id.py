# Generated by Django 2.2.12 on 2020-06-28 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historique', '0002_auto_20200627_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]