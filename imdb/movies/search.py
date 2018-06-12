from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, InnerDoc,Text, Integer,Keyword

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection()


class MovieIndex(DocType):
    name = Text()
    director = Text()
    popularity_99 = Integer()
    imdb_score = Integer()
    genre = Keyword(multi=True)

    class Meta:
        index = 'movie-index'



def bulk_indexing():
    MovieIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.MovieModel.objects.all()))
