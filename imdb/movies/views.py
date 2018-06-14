import json

from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import MovieModel
from  django.core.exceptions import ObjectDoesNotExist
from .models import GenreModel
from .validators import MovieValidator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# Create your views here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q,Search
from elasticsearch_dsl.query import MultiMatch,Match
es = Elasticsearch()


class SearchMovies(APIView):
    serializer = MovieValidator
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        movie = request.GET.get('movie',None)
        if movie:
            queryset = MovieModel.objects.filter(name__icontains = movie)
        else:
            queryset = MovieModel.objects.all()

        serialized = self.serializer(queryset, many=True)
        data = serialized.data
        return Response(data,status=status.HTTP_200_OK)


class ElasticSearch(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        query = request.GET.get('q',None)
        s = Search(using=es,index="movie-index")
        q = Q({"multi_match": {"query": query, "fields": ["name^3", "director"]}})
        s = s.query(q)
        s = s[:300].sort()
        response = s.execute()
        response = response.to_dict()
        return Response(response, status = status.HTTP_200_OK)


class GenreSearch(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        query = request.GET.get('q', None)
        s = Search(using=es, index="movie-index")
        s = s.query('term', genre=query)
        s = s[:300].sort()
        response = s.execute()
        response = response.to_dict()
        return Response(response, status=status.HTTP_200_OK)


class BestMovies(APIView):

    serializer = MovieValidator
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        director = request.GET.get('director',None).title()
        movies = MovieModel.objects.filter(director = director,imdb_score__gte=7).order_by('-imdb_score')
        movies = list(movies)
        if len(movies)==0:
            return Response(data={"message": "The director is not present"}, status=status.HTTP_404_NOT_FOUND)
        response ={}
        for movie in movies:
            serialized = self.serializer(movie)
            response.setdefault('movies',[])
            response["movies"].append(serialized.data)
        return Response(response,status.HTTP_200_OK)


class SearchByGenreAndDirector(APIView):
    serializer = MovieValidator
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        director = request.GET.get('director', None).title()
        genre = request.GET.get('genre',None).title()
        movies = MovieModel.objects.filter(director=director).prefetch_related('genre').order_by('-imdb_score')
        if len(movies)==0:
            return Response(data={"message": "The director has no movie with the given genre"}, status=status.HTTP_404_NOT_FOUND)
        response = {}
        for movie in movies:
            queryset = movie.genre.all()
            for element in queryset:
                if genre in element.genre:
                    serialized = self.serializer(movie)
                    response.setdefault('movies', [])
                    response["movies"].append(serialized.data)
        return Response(response, status.HTTP_200_OK)