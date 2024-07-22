from rest_framework import serializers
from .models import Collection, Movie

from uuid import uuid4


class MovieSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid4)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    genres = serializers.CharField(max_length=255, required=False, allow_blank=True)

    class Meta:
        model = Movie
        fields = ['uuid', 'title', 'description', 'genres']

    def validate_genres(self, value):
        if value == '':
            return None
        return value
        
class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']
        read_only_fields = ['uuid', 'created_at', 'updated_at', 'user']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(**validated_data)

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                uuid=movie_data['uuid'],
                defaults={
                    'title': movie_data.get('title'),
                    'description': movie_data.get('description'),
                    'genres': movie_data.get('genres', '')
                }
            )
            collection.movies.add(movie)
        
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(uuid=movie_data['uuid'], defaults=movie_data)
            instance.movies.add(movie)
        
        return instance
