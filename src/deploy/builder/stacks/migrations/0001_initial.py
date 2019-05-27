# Generated by Django 2.1 on 2019-05-27 10:29

from django.db import migrations, models
import stacks.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('context', models.FileField(upload_to=stacks.models.context_file_path)),
            ],
        ),
    ]
