"""
    artist_concert.py

    Defines the Django model to represent an artist performing at a concert
    """
from django.db import models
from .artist import Artist
from .concert import Concert


class ArtistConcert(models.Model):
    """Represents an instance of a user attending a concert, AKA a ticket"""
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    concert_id = models.ForeignKey(Concert, on_delete=models.CASCADE)
