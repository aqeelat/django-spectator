from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
try:
    # Django >= 1.10
    from django.urls import reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import reverse

from . import BaseRole, Creator, TimeStampedModelMixin
from ..utils import make_sort_name
from .. import managers


class PublicationSeries(TimeStampedModelMixin, models.Model):
    """
    A way to group `Publication`s into series.

    Get its Publications:

        series.publication_set.all()
    """
    title = models.CharField(null=False, blank=False, max_length=255,
            help_text="e.g. 'The London Review of Books'.")
    sort_title = models.CharField(blank=True, max_length=255,
            help_text="e.g. 'Alpine Review, The'. If left blank, will be created automatically on save.")
    url = models.URLField(null=False, blank=True, max_length=255,
            verbose_name='URL', help_text="e.g. 'https://www.lrb.co.uk/'.")

    def save(self, *args, **kwargs):
        if self.sort_title == '':
            self.sort_title = self._make_sort_title(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('sort_title',)
        verbose_name_plural = 'Publication series'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('spectator:publicationseries_detail',
                                                        kwargs={'pk':self.pk})

    def _make_sort_title(self, title):
        return make_sort_name(title, 'thing')


class PublicationRole(BaseRole):
    """
    Linking a creator to a Publication, optionally via their role (e.g.
    'Author', 'Editor', etc.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                    on_delete=models.CASCADE, related_name='publication_roles')

    publication = models.ForeignKey('Publication', on_delete=models.CASCADE,
                                                        related_name='roles')


class Publication(TimeStampedModelMixin, models.Model):
    """
    Get a Publication's creators:

        publication = Publication.objects.get(pk=1)

        # Just the creators:
        for creator in publication.creators.all():
            print(creator.name)

        # Include their roles:
        for role in publication.roles.all():
            print(role.publication, role.creator, role.role_name)

    Get its readings:

        for reading in publication.reading_set.all():
            print(reading.start_date, reading.end_date)
    """

    KIND_CHOICES = (
        ('book', 'Book'),
        ('periodical', 'Periodical'),
    )

    title = models.CharField(null=False, blank=False, max_length=255,
            help_text="e.g. 'Aurora' or 'Vol. 39 No. 4, 16 February 2017'.")
    sort_title = models.CharField(blank=True, max_length=255,
            help_text="e.g. 'Clockwork Orange, A' or 'World Cities, The'. If left blank, will be created automatically on save.")
    series = models.ForeignKey('PublicationSeries', blank=True, null=True,
                                                    on_delete=models.SET_NULL)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES,
                                                        default='book')
    official_url = models.URLField(null=False, blank=True, max_length=255,
            verbose_name='Official URL',
            help_text="Official URL for this book/issue.")
    isbn_uk = models.CharField(null=False, blank=True, max_length=20,
            verbose_name='UK ISBN', help_text="e.g. '0356500489'.")
    isbn_us = models.CharField(null=False, blank=True, max_length=20,
            verbose_name='US ISBN', help_text="e.g. '0316098094'.")
    notes_url = models.URLField(null=False, blank=True, max_length=255,
            verbose_name='Notes URL', help_text="URL of your notes/review.")

    creators = models.ManyToManyField(Creator, through='PublicationRole',
                                                related_name='publications')

    objects = models.Manager()
    # Publications that are currently being read:
    in_progress_objects = managers.InProgressPublicationsManager()
    # Publications that haven't been started (have no Readings):
    unread_objects = managers.UnreadPublicationsManager()

    def save(self, *args, **kwargs):
        if self.sort_title == '':
            self.sort_title = self._make_sort_title(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('sort_title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('spectator:publication_detail', kwargs={'pk':self.pk})

    def get_current_reading(self):
        try:
            return self.reading_set.filter(end_date__isnull=True)[0]
        except IndexError:
            pass

    @property
    def amazon_uk_url(self):
        url = ''
        if self.isbn_uk:
            url = 'https://www.amazon.co.uk/gp/product/{}/'.format(self.isbn_uk)
            if hasattr(settings, 'SPECTATOR_AMAZON') and 'uk' in settings.SPECTATOR_AMAZON:
                url = '{}?tag={}'.format(url, settings.SPECTATOR_AMAZON['uk'])
        return url

    @property
    def amazon_us_url(self):
        url = ''
        if self.isbn_us:
            url = 'https://www.amazon.com/dp/{}/'.format(self.isbn_us)
            if hasattr(settings, 'SPECTATOR_AMAZON') and 'us' in settings.SPECTATOR_AMAZON:
                url = '{}?tag={}'.format(url, settings.SPECTATOR_AMAZON['us'])
        return url

    @property
    def amazon_urls(self):
        urls = []
        if self.isbn_uk:
            urls.append({
                'url': self.amazon_uk_url,
                'name': 'Amazon.co.uk',
                'country': 'UK',
            })
        if self.isbn_us:
            urls.append({
                'url': self.amazon_us_url,
                'name': 'Amazon.com',
                'country': 'USA',
            })
        return urls

    @property
    def has_urls(self):
        "Handy for templates."
        if self.isbn_uk or self.isbn_us or self.official_url or self.notes_url:
            return True
        else:
            return False

    def _make_sort_title(self, title):
        return make_sort_name(title, 'thing')


class Reading(TimeStampedModelMixin, models.Model):
    """
    A period when a Publication was read.
    """
    # Via https://www.flickr.com/services/api/misc.dates.html
    DATE_GRANULARITIES = (
        # (0, 'Y-m-d H:i:s'),
        (3, 'Y-m-d'),
        (4, 'Y-m'),
        (6, 'Y'),
        # (8, 'Circa...'),
    )

    publication = models.ForeignKey('Publication', null=False, blank=False)

    start_date = models.DateField(null=True, blank=True)
    start_granularity = models.PositiveSmallIntegerField(null=False,
            blank=False, default=3, choices=DATE_GRANULARITIES)
    end_date = models.DateField(null=True, blank=True)
    end_granularity = models.PositiveSmallIntegerField(null=False,
            blank=False, default=3, choices=DATE_GRANULARITIES)
    is_finished = models.BooleanField(default=False,
            help_text="Did you finish the publication?")

    objects = managers.EndDateAscendingReadingsManager()
    objects_desc = managers.EndDateDescendingReadingsManager()

    def __str__(self):
        return '{} ({} to {})'.format(
                            self.publication, self.start_date, self.end_date)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                    "A Reading's end date can't be before its start date.")

