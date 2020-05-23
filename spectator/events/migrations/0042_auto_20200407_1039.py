# Generated by Django 3.0.5 on 2020-04-07 10:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0041_event_ticket"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venue",
            name="cinema_treasures_id",
            field=models.PositiveIntegerField(
                blank=True,
                help_text='Optional. ID of a cinema at\n<a href="http://cinematreasures.org/">Cinema Treasures</a>.',  # noqa: E501
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="work",
            name="imdb_id",
            field=models.CharField(
                blank=True,
                help_text="Starts with 'tt', e.g. 'tt0100842'.\nFrom <a href=\"https://www.imdb.com\">IMDb</a>.",  # noqa: E501
                max_length=12,
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_imdb_id",
                        message='IMDb ID should be like "tt1234567"',
                        regex="^tt\\d{7,10}$",
                    )
                ],
                verbose_name="IMDb ID",
            ),
        ),
    ]
