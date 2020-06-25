
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
