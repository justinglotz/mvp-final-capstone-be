"""
    concert.py

    Defines the Django model for a concert, including:
    artist id, venue id, tour name, date and time
    """
from django.db import models
from .venue import Venue


class Concert(models.Model):
    """Represents a concert in the database"""
    venue_id = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
