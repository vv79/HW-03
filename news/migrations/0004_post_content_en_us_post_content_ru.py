# Generated by Django 4.0.8 on 2022-11-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_post_title_en_us_post_title_ru'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='content_ru',
            field=models.TextField(null=True),
        ),
    ]
