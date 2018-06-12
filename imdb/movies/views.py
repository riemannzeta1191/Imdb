import json

from rest_framework.response import Response
from rest_framework import status
from .models import MovieModel
from .models import GenreModel
from .validators import MovieValidator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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

    def get(self,request):
        director = request.GET.get('director',None)
        movies = MovieModel.objects.filter(director = director,imdb_score__gte=7)
        movies = list(movies)
        response ={}
        for movie in movies:
            serialized = self.serializer(movie)
            response.setdefault('movies',[])
            response["movies"].append(serialized.data)
        return Response(response,status.HTTP_200_OK)