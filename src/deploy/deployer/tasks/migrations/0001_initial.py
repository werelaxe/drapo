# Generated by Django 2.1 on 2019-06-04 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filecontexts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('error', 'Error was occurred while processing'), ('enqueued', 'Enqueued'), ('ready', 'Stack successfully built and pushed. Task is ready to deploy'), ('processing', 'Processing'), ('deployed', 'Deployed'), ('added', 'Task added')], max_length=10)),
                ('error_text', models.TextField()),
                ('config_text', models.TextField()),
                ('filecontext', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='filecontexts.FileContext')),
            ],
        ),
    ]
