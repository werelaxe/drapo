# Generated by Django 2.1 on 2019-06-04 20:22

from django.db import migrations, models
import filecontexts.models


class Migration(migrations.Migration):

    dependencies = [
        ('filecontexts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filecontext',
            name='dc_file',
            field=models.FileField(upload_to=filecontexts.models.dc_file_path),
        ),
    ]
