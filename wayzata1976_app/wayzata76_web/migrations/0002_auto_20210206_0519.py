# Generated by Django 3.1.5 on 2021-02-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayzata76_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='middle_initial',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
