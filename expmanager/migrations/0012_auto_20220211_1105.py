# Generated by Django 3.1.2 on 2022-02-11 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expmanager', '0011_auto_20220211_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemical',
            name='SMILES',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
    ]
