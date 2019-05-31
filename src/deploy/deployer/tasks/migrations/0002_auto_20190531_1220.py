# Generated by Django 2.1 on 2019-05-31 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('error', 'Error was occurred while processing'), ('enqueued', 'Enqueued'), ('ready', 'Stack successfully built and pushed. Task is ready to deploy'), ('processing', 'Processing'), ('deployed', 'Deployed'), ('added', 'Task added without file context')], max_length=10),
        ),
    ]
