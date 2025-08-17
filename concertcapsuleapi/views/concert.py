"""View module for handling requests about concerts"""
from django.http import HttpResponseServerError
import traceback
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from concertcapsuleapi.models import Concert, Venue, ArtistConcert, Artist


class ConcertView(ViewSet):
    """Concerts View"""

    def retrieve(self, request, pk):
        """GET a single concert"""
        try:
            concert = Concert.objects.get(pk=pk)
            serializer = ConcertSerializer(concert)
            return Response(serializer.data)
        except Concert.DoesNotExist:
            return Response({"error": "Concert not found"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET all concerts"""
        uid = request.query_params.get("uid", None)

        if uid:
            concerts = Concert.objects.filter(uid=uid)
        else:
            concerts = Concert.objects.all()
        serializer = ConcertSerializer(concerts, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """DELETE a concert"""
        try:
            concert = Concert.objects.get(pk=pk)
            concert.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Concert.DoesNotExist:
            return Response({"error": "Concert not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Handle PUT requests to update an existing concert"""
        try:
            concert = Concert.objects.get(pk=pk)
            venue = Venue.objects.get(pk=request.data["venue"])

            # Update fields
            concert.uid = request.data["uid"]
            concert.venue_id = venue.id
            concert.date = request.data["date"]

            # Update artists in the join table
            artist_ids = request.data.get("artists", [])
            # Remove existing artist associations
            ArtistConcert.objects.filter(concert=concert).delete()
            # Add new artist associations
            for artist_id in artist_ids:
                artist = Artist.objects.get(pk=artist_id)
                ArtistConcert.objects.create(
                    concert_id=concert.id,
                    artist_id=artist.id
                )

            concert.save()
            serializer = ConcertSerializer(concert)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Concert.DoesNotExist:
            return Response({'message': 'Concert not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """POST a new concert"""
        try:
            # Fetch related venue
            venue = Venue.objects.get(pk=request.data["venue"])
            # Create Concert
            concert = Concert.objects.create(
                venue_id=venue.id,
                uid=request.data["uid"],
                date=request.data["date"],
            )

            # Link artists via join table
            artist_ids = request.data.get("artists", [])
            for artist_id in artist_ids:
                artist = Artist.objects.get(pk=artist_id)
                ArtistConcert.objects.create(
                    concert_id=concert.id,
                    artist_id=artist.id
                )

            serializer = ConcertSerializer(concert)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Venue.DoesNotExist:
            return Response({"error": "Venue not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Artist.DoesNotExist:
            return Response({"error": "Artist not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']


class ConcertSerializer(serializers.ModelSerializer):
    artists = serializers.SerializerMethodField()

    class Meta:
        model = Concert
        fields = ('id', 'date', 'venue', 'artists')
        depth = 1

    def get_artists(self, concert):
        artist_concerts = ArtistConcert.objects.filter(concert=concert)
        artists = [ac.artist for ac in artist_concerts]
        return ArtistSerializer(artists, many=True).data
