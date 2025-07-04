# Generated by Django 5.2.1 on 2025-06-17 14:38

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0035_alter_entity_options_file_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='file',
            name='objectives',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Objectives'),
        ),
    ]
