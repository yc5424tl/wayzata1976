# Generated by Django 3.1.5 on 2021-01-21 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wayzata76_web', '0004_auto_20210121_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspostimage',
            name='news_post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='news_post_image', to='wayzata76_web.newspost'),
        ),
    ]
