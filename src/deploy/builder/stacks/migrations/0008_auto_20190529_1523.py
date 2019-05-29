# Generated by Django 2.1 on 2019-05-29 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stacks', '0007_auto_20190529_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stack',
            name='status',
            field=models.CharField(choices=[('Error', 'Error'), ('Enqueued', 'Enqueued'), ('Successfully built and pushed', 'Successfully built and pushed'), ('Processing', 'Processing')], max_length=2),
        ),
    ]
