from django.db import models
from .search import MovieIndex
# Create your models here.


class GenreModel(models.Model):
    genre = models.CharField(max_length=200)

    def __str__(self):
        return self.genre


class MovieModel(models.Model):
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    popularity_99 = models.DecimalField(max_digits=4, decimal_places=1)
    imdb_score = models.DecimalField(max_digits=4, decimal_places=1)
    genre = models.ManyToManyField(GenreModel)

    def __str__(self):
        return "%s (%s)" % (self.name, ", ".join(genre.genre
                                                 for genre in self.genre.all()))

    def indexing(self):
        genre = []
        movies = MovieModel.objects.filter(name=self.name)
        movies = list(movies)
        for movie in movies:
            genre_model = movie.genre.all()
            genre_model = list(genre_model)
            for gen in genre_model:
                genre.append(gen.genre)
        obj = MovieIndex(
          meta={'id': self.id},
           name = self.name,
           director = self.director,
           popularity_99 = self.popularity_99,
           imdb_score = self.imdb_score,
           genre = genre
       )
        obj.save()
        return obj.to_dict(include_meta=True)

