# Generated by Django 4.1.2 on 2023-12-19 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('virtualgovservices', '0021_remove_dokument_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verfahren',
            name='verantwortlicher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='virtualgovservices.beamter'),
        ),
    ]