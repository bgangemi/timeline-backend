# Generated by Django 5.2.1 on 2025-05-21 12:55

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0010_file_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='description',
            new_name='notes',
        ),
        migrations.AlterField(
            model_name='file',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
