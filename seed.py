
from sqlalchemy import func
from model import User
from model import MovieList
from model import Movie
from model import Genre
from model import GenresMovies

from model import connect_to_db, db
from server import app

import csv

from datetime import datetime 



def load_movies():
    """Load movies from u.item into database."""


    print("Movies")

    Movie.query.delete()

    genre_list = []

    with open("seed_data/movies_metadata.csv",newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            genre_list = []

            if row['title'] in (None, ""):
                continue
            else:
                title = row['title']
            genres = row['genres']
            genres = eval(genres)
            for genre in genres:
                genre_id = genre['id']
                genre_name = genre['name']
                exists = Genre.query.get(genre_id)

                if exists == None:

                    new_genre = Genre (genre_id = genre_id, gname = genre_name)
                    genre_list.append(new_genre)
                    db.session.add(new_genre)
                else:
                    genre_list.append(exists)
                    continue


            imdb_id = row['imdb_id']
            plot = row['overview']
            if row['poster_path'] in (None, ""):
                continue
            else:
                poster = 'https://image.tmdb.org/t/p/w500' + row['poster_path']
            if row['release_date'] in (None, ""):
                continue
            else:
                released_at = row['release_date'][:4]


            movie = Movie (imdb_id = imdb_id, 
                            title = title, plot = plot,
                            released_at = released_at, 
                            poster=poster)

            movie.genres.extend(genre_list)
            db.session.add(movie)
            
            

    db.session.commit()
    print("Successfully added all movies")









if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_movies()