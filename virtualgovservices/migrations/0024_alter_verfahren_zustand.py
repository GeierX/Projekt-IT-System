# Generated by Django 4.1.2 on 2023-12-19 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualgovservices', '0023_beamter_nr_zuständigkeit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verfahren',
            name='zustand',
            field=models.CharField(default='Antrag gestellt', max_length=100),
        ),
    ]
