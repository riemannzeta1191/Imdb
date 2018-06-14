from django.conf.urls import url, include
from django.contrib import admin

from .import views
from .views import SearchMovies,ElasticSearch,GenreSearch,BestMovies,SearchByGenreAndDirector,DeleteMovie,ReadMovie
app_name = "movies"

urlpatterns = [
    url(r'^movies/$', SearchMovies.as_view(), name='index'),
    url(r'^elastic/$', ElasticSearch.as_view(), name='elastic'),
    url(r'^elastic/genre/$', GenreSearch.as_view(), name='genre'),
    url(r'^best/$', BestMovies.as_view(), name='best'),
    url(r'^search/genre/$', SearchByGenreAndDirector.as_view(), name='search_genre'),
    url(r'^movie/(?P<id>[0-9]+)/$', ReadMovie.as_view(), name='movie_read'),
    url(r'^movie/(?P<id>[0-9]+)/delete/$', DeleteMovie.as_view(), name='movie_delete'),
]
