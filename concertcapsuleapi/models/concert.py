"""
    concert.py

    Defines the Django model for a concert, including:
    venue id, date and uid
    """
from django.db import models
from .venue import Venue


class Concert(models.Model):
    """Represents a concert in the database"""
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    date = models.CharField(max_length=50)
    uid = models.CharField(max_length=50)
