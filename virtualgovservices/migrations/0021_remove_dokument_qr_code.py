# Generated by Django 4.1.2 on 2023-12-19 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtualgovservices', '0020_beamter_anrede_beamter_email_beamter_nachname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dokument',
            name='qr_code',
        ),
    ]
