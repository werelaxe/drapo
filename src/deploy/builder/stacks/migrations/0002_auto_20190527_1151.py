# Generated by Django 2.1 on 2019-05-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stacks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stack',
            name='id',
        ),
        migrations.AlterField(
            model_name='stack',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
