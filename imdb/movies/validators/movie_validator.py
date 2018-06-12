from rest_framework import serializers
from ..models import MovieModel
from ..models import GenreModel


class GenreValidator(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = '__all__'


class MovieValidator(serializers.ModelSerializer):

    genre = GenreValidator(many=True)

    class Meta:
        model = MovieModel
        fields = ('name', 'imdb_score', 'popularity_99', 'director', 'genre')