# Generated by Django 3.1.5 on 2021-02-15 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayzata76_web', '0003_auto_20210211_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresult',
            name='food',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]