# Generated by Django 4.1.2 on 2024-01-16 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualgovservices', '0028_beamter_raum_beamter_rolle_buerger_rolle'),
    ]

    operations = [
        migrations.AddField(
            model_name='beamter',
            name='profileimg',
            field=models.ImageField(default='/virtualgovservices/profile_images/avatar.jpg', upload_to='virtualgovservices/profile_images/'),
        ),
    ]
