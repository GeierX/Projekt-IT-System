# Generated by Django 4.1.2 on 2024-01-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualgovservices', '0025_alter_buerger_geburtsdatum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buerger',
            name='geburtsdatum',
            field=models.DateField(blank=True, default='1995-01-01'),
        ),
    ]
