from django.contrib import admin

# Register your models here.
from .models import MovieModel, GenreModel


class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'imdb_score', 'director', 'popularity_99']
    list_filter = ['genre']
    search_fields = ['name', 'director']


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(MovieModel, MovieAdmin)
admin.site.register(GenreModel, GenreAdmin)