# Generated by Django 4.1.2 on 2024-01-23 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualgovservices', '0029_beamter_profileimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='dokument',
            name='bemerkungen',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dokument',
            name='titel',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dokument',
            name='inhalt',
            field=models.TextField(blank=True, null=True),
        ),
    ]