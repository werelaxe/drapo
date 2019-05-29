# Generated by Django 2.1 on 2019-05-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stacks', '0006_stack_error_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stack',
            name='status',
            field=models.CharField(choices=[('ERR', 'Error'), ('ENQ', 'Enqueued'), ('PSH', 'Successfully built and pushed'), ('PRC', 'Processing')], max_length=2),
        ),
    ]
