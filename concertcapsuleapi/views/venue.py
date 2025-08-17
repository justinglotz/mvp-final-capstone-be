"""View module for handling requests about venues"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from concertcapsuleapi.models import Venue


class VenueView(ViewSet):
    """Venues View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single venue

        Returns:
        Response -- JSON serialized venue
        """
        venue = Venue.objects.get(pk=pk)
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all venues

        Returns:
            Response -- JSON serialized list of venue types
  """
        venues = Venue.objects.all()

        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for a venue

        Returns:
            Response -- Empty body with 204 status code
            """
        venue = Venue.objects.get(pk=pk)
        venue.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class VenueSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Venue
        fields = ('id', 'name', 'city', 'state')
        depth = 1
