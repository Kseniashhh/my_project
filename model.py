"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)


    
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
                "email": self.email
                }


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User username={self.user_id} email={self.email}>"


# Put your Movie and Rating model classes here.

class Movie(db.Model):
    """ Movies and its info """

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    imdb_id = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    plot = db.Column(db.String(1000),nullable=False)
    released_at = db.Column(db.String(200), nullable=True)
    poster = db.Column(db.String(200), nullable=False)

    genres = db.relationship('Genre', secondary = "gen_movies",backref = 'movies')



    def mov_serial(self):
       """Return object data in easily serializeable format"""
       return {
                "movie_id": self.movie_id,
                "title": self.title,
                "plot": self.plot,
                "released_at": self.released_at,
                "poster": self.poster
                }


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Movie movie_id={self.movie_id} title={self.title}>"



class Genre (db.Model):
    """ Genres table """

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True)
    gname = db.Column(db.String(30), nullable=False)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Genre genre_id={self.genre_id} genre_name={self.gname}>"



class GenresMovies (db.Model):
    """ MovieIDs and genres mapping """

    __tablename__ = "gen_movies"

    mg_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)

    
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<movie_id= {self.movie_id} genre_id={self.genre_id}>"





class MovieList(db.Model):
    """ Favorite, recommended, planned to watch movies by user """

    __tablename__ = "movie_list"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    date_added = db.Column(db.DateTime, nullable=False)
    interested = db.Column(db.Boolean, nullable=True)
    shared = db.Column(db.Boolean, nullable=True)


    user = db.relationship('User', backref = 'movie_list')
    movie = db.relationship('Movie', backref = 'movie_list')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Movie/user user_id={self.user_id} movie={self.movie_id}>"


class Food(db.Model):
    """ Food places and its info """

    __tablename__ = "foods"

    food_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yelp_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(1000),nullable=True)
    rating = db.Column(db.String(1000),nullable=True)
    address = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=False)




    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Food food_id={self.food_id} name={self.name}>"





class FoodList(db.Model):
    """ Favorite, recommended, planned to visit food places by user """

    __tablename__ = "food_list"

    flist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.food_id'))
    date_added = db.Column(db.DateTime, nullable=False)
    interested = db.Column(db.Boolean, nullable=True)
    shared = db.Column(db.Boolean, nullable=True)


    user = db.relationship('User', backref = 'food_list')
    food = db.relationship('Food', backref = 'food_list')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Food/user user_id={self.user_id} food={self.food_id}>"



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///whatiwant'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)




if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")