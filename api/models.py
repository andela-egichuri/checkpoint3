from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Bucketlist(models.Model):
    """Stores Bucketlists."""

    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bucketlists'
    )

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return '%s' % (self.name)


class Item(models.Model):
    """Stores Bucketlist Items"""

    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)
    bucketlist = models.ForeignKey(
        Bucketlist, on_delete=models.CASCADE, related_name='items'
    )

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return '%s' % (self.name)
