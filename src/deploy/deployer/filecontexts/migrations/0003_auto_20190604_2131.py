# Generated by Django 2.1 on 2019-06-04 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filecontexts', '0002_auto_20190604_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='filecontext',
            name='error_text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filecontext',
            name='status',
            field=models.CharField(choices=[('enqueued', 'Enqueued'), ('error', 'Error was occurred while checking context correctness'), ('processing', 'Processing'), ('correct', 'File context passed the correctness checking')], default='', max_length=10),
            preserve_default=False,
        ),
    ]
