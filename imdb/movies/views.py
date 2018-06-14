

from rest_framework.response import Response
from rest_framework import status
from .models import MovieModel
from  django.core.exceptions import ObjectDoesNotExist
from .validators import MovieValidator
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q,Search
es = Elasticsearch()
# Create your views here.


class SearchMovies(generics.ListCreateAPIView):
    serializer_class = MovieValidator
    queryset = MovieModel.objects.all()

    def list(self, request, *args, **kwargs):
        movie = request.GET.get('movie',None)
        queryset = self.get_queryset()
        if movie:
            queryset = queryset.filter(name__icontains = movie)

        serialized = self.serializer_class(queryset,many=True)
        data = serialized.data
        return Response(data,status=status.HTTP_200_OK)


class ElasticSearch(GenericAPIView):

    def get(self, request):
        query = request.GET.get('q',None)
        s = Search(using=es,index="movie-index")
        q = Q({"multi_match": {"query": query, "fields": ["name^3", "director"]}})
        s = s.query(q)
        s = s[:300].sort()
        response = s.execute()
        response = response.to_dict()
        response = response['hits']['hits']
        return Response(response, status = status.HTTP_200_OK)


class GenreSearch(APIView):

    def get(self, request):
        query = request.GET.get('q', None)
        s = Search(using=es, index="movie-index")
        s = s.query('term', genre=query)
        s = s[:300].sort()
        response = s.execute()
        response = response.to_dict()
        response = response['hits']['hits']
        return Response(response, status=status.HTTP_200_OK)


class BestMovies(APIView):

    serializer = MovieValidator

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


class MovieCRUD(APIView):
    serializer = MovieValidator
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, id):
        try:
            movie = MovieModel.objects.get(id=id)
            serialized = self.serializer(movie)
            data = serialized.data
            return Response(data=data,status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(data={"message": "Given movie is not present"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            movie = MovieModel.objects.get(id=id)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            print(str(e))
            return Response(data={"message": "Given movie is not present"}, status=status.HTTP_404_NOT_FOUND)
