# Generated by Django 4.1.2 on 2023-12-12 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtualgovservices', '0013_remove_verfahren_antragssteller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verfahren',
            name='verantwortlicher',
        ),
    ]