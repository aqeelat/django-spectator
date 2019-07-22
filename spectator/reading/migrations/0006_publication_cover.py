# Generated by Django 2.2.3 on 2019-07-22 16:47

from django.db import migrations, models
import spectator.reading.models


class Migration(migrations.Migration):

    dependencies = [
        ('spectator_reading', '0005_auto_20180125_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to=spectator.reading.models.publication_upload_path),
        ),
    ]
