# Imdb
 The Imdb application lists movies alongwith their respective director, popularity,genre and imdb score.
 API's are built using permissions on the basis whether it's a superuser user or not
 
API Reference:
https://ancient-gorge-18685.herokuapp.com/imdb/movies/ 
Lists all movies.The api is a generic list view

https://ancient-gorge-18685.herokuapp.com/imdb/elastic/?q=Shadow of a Doubt

ngrok link : -http://c4418e3f.ngrok.io/imdb/elastic/?q=Shadow of a Doubt 
which exposes the elasticsearch backend
Lists movies based upon movie name or director name through partial search

https://ancient-gorge-18685.herokuapp.com/imdb/elastic/genre/?q=drama

http://c4418e3f.ngrok.io/imdb/elastic/genre/?q=drama
Lists movies based upon genre

https://ancient-gorge-18685.herokuapp.com/imdb/best/?director=stanley%20kubrick
Lists movies by directors if the imdb score is greater than equal to 7

https://ancient-gorge-18685.herokuapp.com/imdb/search/genre/?director=alfred%20Hitchcock&genre=mystery
lists movies by any director based upon a single genre

https://ancient-gorge-18685.herokuapp.com/imdb/movie/19/
The above api returns the movie document based upon the id and also let's one delete the document if it's an
aunthenticated user.The above api consists of two verbs GET and DELETE
