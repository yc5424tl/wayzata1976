# Generated by Django 3.1.5 on 2021-03-16 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayzata76_web', '0009_auto_20210316_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagepostimage',
            name='caption',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
