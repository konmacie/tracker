from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Service(models.Model):

    SCRAPPER_REDDIT = 1
    SCRAPPER_RSS = 2

    _SCRAPPER_TYPES = (
        (SCRAPPER_REDDIT, 'Reddit'),
        (SCRAPPER_RSS, 'RSS'),
    )

    name = models.CharField(max_length=255)
    url = models.URLField()
    last_run = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    scraper = models.IntegerField(default=SCRAPPER_REDDIT,
                                  choices=_SCRAPPER_TYPES)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='services')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('service', kwargs={'pk': self.pk})


class ScraperRunLog(models.Model):

    STATUS_RUNNING, STATUS_FINISHED = 1, 2

    _STATUS_TYPES = (
        (STATUS_RUNNING, 'Running'),
        (STATUS_FINISHED, 'Finished')
    )

    timestamp_start = models.DateTimeField(auto_now_add=True)
    timestamp_end = models.DateTimeField(null=True)
    status = models.SmallIntegerField(default=STATUS_RUNNING,
                                      choices=_STATUS_TYPES)

    def __str__(self):
        return str(self.timestamp_start)


class Post(models.Model):

    service = models.ForeignKey(
        Service, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    guid = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    run_log = models.ForeignKey(
        ScraperRunLog, null=True, default=None, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-timestamp', '-id')

    def __str__(self):
        return str(self.title)
