# Generated by Django 2.1 on 2019-05-31 12:00

from django.db import migrations, models
import tasks.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('context', models.FileField(upload_to=tasks.models.context_file_path)),
                ('download_url', models.TextField()),
                ('status', models.CharField(choices=[('error', 'Error was occurred while processing'), ('enqueued', 'Enqueued'), ('ready', 'Stack successfully built and pushed. Task is ready to deploy'), ('processing', 'Processing'), ('deployed', 'Deployed')], max_length=10)),
                ('error_text', models.TextField()),
            ],
        ),
    ]
