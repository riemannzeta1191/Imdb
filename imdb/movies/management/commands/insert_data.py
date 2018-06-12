import json
from django.core.management.base import BaseCommand
from ...models import GenreModel,MovieModel

from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        filepath = "BASE_DIR" + '/imdb.json'
        with open(filepath, 'r') as f:
            raw_data = f.read()
            data = json.loads(raw_data)
            movie_dict = {}
            for movie_item in data:
                movie_dict['name'] = movie_item.get('name')
                movie_dict['popularity_99'] = movie_item.get('99popularity')
                movie_dict['director'] = movie_item.get('director')
                movie_dict['imdb_score'] = movie_item.get('imdb_score')
                movie, created = MovieModel.objects.get_or_create(**movie_dict)
                genre_list = movie_item.get('genre')
                for name in genre_list:
                    name = name.strip()
                    genre, created = GenreModel.objects.get_or_create(genre=name)
                    movie.genre.add(genre)
                movie.save()
