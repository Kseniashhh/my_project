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
    rated_at = db.Column(db.Integer, nullable=True)
    interested = db.Column(db.Boolean, nullable=True)
    recommended = db.Column(db.Boolean, nullable=True)


    user = db.relationship('User', backref = 'movie_list')
    movie = db.relationship('Movie', backref = 'movie_list')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Movie/user user_id={self.user_id} movie={self.movie_id}>"


# class Rating(db.Model):
#     """ Movies and its info """

#     __tablename__ = "rating"

#     rating_id = db.Column(db.Integer, 
#                         autoincrement=True, 
#                         primary_key=True)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     score = db.Column(db.Integer, nullable=False)

#     # Define relationship to user
#     user = db.relationship("User",
#                            backref=db.backref("ratings",
#                                               order_by=rating_id))

#     # Define relationship to movie
#     movie = db.relationship("Movie",
#                             backref=db.backref("ratings",
#                                                order_by=rating_id))


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return f"<Rating rating_id={self.rating_id} score={self.score}>"

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