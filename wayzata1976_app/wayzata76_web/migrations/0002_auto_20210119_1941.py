# Generated by Django 3.1.5 on 2021-01-20 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayzata76_web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyresult',
            old_name='location_idea',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='surveyresult',
            old_name='misc_idea',
            new_name='misc',
        ),
        migrations.RenameField(
            model_name='surveyresult',
            old_name='music_idea',
            new_name='music',
        ),
        migrations.AddField(
            model_name='surveyresult',
            name='music_other',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
