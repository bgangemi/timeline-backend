# Generated by Django 5.2.1 on 2025-06-04 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0022_file_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
