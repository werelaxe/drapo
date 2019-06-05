# Generated by Django 2.1 on 2019-06-04 20:21

from django.db import migrations, models
import filecontexts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('context', models.FileField(upload_to=filecontexts.models.context_file_path)),
                ('dc_file', models.FileField(upload_to=filecontexts.models.context_file_path)),
                ('download_url', models.TextField()),
            ],
        ),
    ]
