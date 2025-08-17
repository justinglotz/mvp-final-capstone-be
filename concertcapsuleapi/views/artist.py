"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from concertcapsuleapi.models import Artist


class ArtistView(ViewSet):
    """Artists View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist

        Returns:
        Response -- JSON serialized artist
        """
        artist = Artist.objects.get(pk=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all artists

        Returns:
            Response -- JSON serialized list of artist types
  """
        artists = Artist.objects.all()

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for a artist

        Returns:
            Response -- Empty body with 204 status code
            """
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Artist
        fields = ('id', 'name')
        depth = 1
