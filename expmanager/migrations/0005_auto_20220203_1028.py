# Generated by Django 3.2.5 on 2022-02-03 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expmanager', '0004_remove_chemical_opened_under_air'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chemical',
            old_name='URL',
            new_name='reference',
        ),
        migrations.RenameField(
            model_name='mixture',
            old_name='URL',
            new_name='reference',
        ),
    ]
