from django.db import models

from spectator.core.fields import NaturalSortField


class TitleModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    title_sort = NaturalSortField("title")


class PersonModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    name_sort = NaturalSortField("name")
    sort_as = "person"
