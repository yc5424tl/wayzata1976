# Generated by Django 3.1.5 on 2021-01-22 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wayzata76_web', '0005_auto_20210121_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='zip',
            new_name='zip_code',
        ),
    ]
