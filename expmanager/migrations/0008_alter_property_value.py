# Generated by Django 3.2.5 on 2022-02-03 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expmanager', '0007_mixturecomponent_molar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='value',
            field=models.CharField(max_length=2000),
        ),
    ]
