<<<<<<< HEAD
# Generated by Django 2.2.12 on 2020-06-10 01:18
=======
# Generated by Django 2.2.12 on 2020-06-07 11:04
>>>>>>> 722855a1e86749d7f9a23ae79338e0b66cefd7a2

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transformToLD', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='file_path',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
