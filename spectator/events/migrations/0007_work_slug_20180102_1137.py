# Generated by Django 2.0 on 2018-01-02 11:37

from django.db import migrations, models
from django.conf import settings
from hashids import Hashids


def generate_slug(value):
    "A copy of spectator.core.models.SluggedModelMixin._generate_slug()"
    alphabet = "abcdefghijkmnopqrstuvwxyz23456789"
    salt = "Django Spectator"

    if hasattr(settings, "SPECTATOR_SLUG_ALPHABET"):
        alphabet = settings.SPECTATOR_SLUG_ALPHABET

    if hasattr(settings, "SPECTATOR_SLUG_SALT"):
        salt = settings.SPECTATOR_SLUG_SALT

    hashids = Hashids(alphabet=alphabet, salt=salt, min_length=5)

    return hashids.encode(value)


def set_slug(apps, schema_editor, class_name):
    """
    Create a slug for each Work already in the DB.
    """
    Cls = apps.get_model("spectator_events", class_name)

    for obj in Cls.objects.all():
        obj.slug = generate_slug(obj.pk)
        obj.save(update_fields=["slug"])


def set_classicalwork_slug(apps, schema_editor):
    set_slug(apps, schema_editor, "ClassicalWork")


def set_dancepiece_slug(apps, schema_editor):
    set_slug(apps, schema_editor, "DancePiece")


def set_movie_slug(apps, schema_editor):
    set_slug(apps, schema_editor, "Movie")


def set_play_slug(apps, schema_editor):
    set_slug(apps, schema_editor, "Play")


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0006_event_slug_20180102_1127"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classicalwork",
            name="slug",
            field=models.SlugField(blank=True, default="a", max_length=10),
            preserve_default=False,
        ),
        migrations.RunPython(set_classicalwork_slug),
        migrations.AlterField(
            model_name="dancepiece",
            name="slug",
            field=models.SlugField(blank=True, default="a", max_length=10),
            preserve_default=False,
        ),
        migrations.RunPython(set_dancepiece_slug),
        migrations.AlterField(
            model_name="movie",
            name="slug",
            field=models.SlugField(blank=True, default="a", max_length=10),
            preserve_default=False,
        ),
        migrations.RunPython(set_movie_slug),
        migrations.AlterField(
            model_name="play",
            name="slug",
            field=models.SlugField(blank=True, default="a", max_length=10),
            preserve_default=False,
        ),
        migrations.RunPython(set_play_slug),
    ]
