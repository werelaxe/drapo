# Generated by Django 2.1 on 2019-05-29 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks', '0004_stack_year_in_school'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stack',
            old_name='year_in_school',
            new_name='status',
        ),
    ]