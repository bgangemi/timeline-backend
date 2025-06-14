# Generated by Django 5.2.1 on 2025-05-22 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0015_uploadeddocument_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date_approx_level',
            field=models.CharField(choices=[('none', 'Exact'), ('day', 'Approximate day'), ('week', 'Approximate week'), ('month', 'Approximate month'), ('year', 'Approximate year'), ('unknown', 'Unknown/very vague')], default='none', max_length=10),
        ),
    ]
