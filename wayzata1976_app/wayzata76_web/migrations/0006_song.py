# Generated by Django 3.1.5 on 2021-03-04 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayzata76_web', '0005_auto_20210216_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('artist', models.CharField(max_length=200)),
                ('position', models.PositiveSmallIntegerField()),
                ('peak', models.PositiveSmallIntegerField()),
                ('weeks_peak', models.PositiveSmallIntegerField()),
                ('weeks_top10', models.PositiveSmallIntegerField()),
                ('weeks_top40', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
