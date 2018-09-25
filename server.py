from jinja2 import StrictUndefined

import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Movie, MovieList, Genre, GenresMovies, connect_to_db, db

import requests

from imdb import IMDb

import random

import json

import guidebox

from datetime import datetime 



# guidebox.api_key = os.environ['GUIDEBOX_TRIAL_KEY']
# guidebox.region = "US"

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined





######################################################################

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")



#####################################################################

@app.route('/register')
def signup_page():
    """ Page where user signs up """

    return render_template("registration.html")

#####################################################################

@app.route('/username_check')
def if_username_exists():
    """ Checks if username is taken """

    username = request.args.get("username")

    QUERY = """
        SELECT username
        FROM users
        WHERE username = :username
        """

    db_cursor = db.session.execute(QUERY, {'username': username})
    row = db_cursor.fetchone()

    if row:
        user_name = row[0]
    else:
        user_name = "None"


    return user_name


#####################################################################


@app.route("/user_added")
def user_signsUp():
    """ Register new user, ignore existing"""

    email = request.args.get("email") 
    pswd = request.args.get("password")
    username = request.args.get("username")
    

    user_exists = if_user_exists(email)

    if user_exists == None:
        add_user(username,email, pswd)
        user_exists = if_user_exists(email)
        session['user'] = user_exists[0]
        return redirect("/")
    else:  
        flash("This user is aleady registered. Please log in")
        return redirect("/login")




def if_user_exists(email):
    """ Given email address checks if user already exists"""

    QUERY = """
        SELECT user_id, email
        FROM users
        WHERE email = :email
        """

    db_cursor = db.session.execute(QUERY, {'email': email})
    row = db_cursor.fetchone()

    return row




def add_user(username, email, password):
    """ Given email and password add new user to users table"""

    now = datetime.now()
    created_date = now.strftime('%Y/%m/%d %H:%M:%S')

    QUERY = """
        INSERT INTO users (email, password, username, created_date)
        VALUES (:email, :password, :username, :created_date)
        """

    db_cursor = db.session.execute(QUERY, {'email': email, 
                                'password': password, 'username': username, 'created_date':created_date})

    db.session.commit()



####################################################################


@app.route("/login")
def user_logIn():
    """ Log in form"""

    return redirect("/")


####################################################################


@app.route("/logout")
def user_logOut():
    """ log out current user """
    
    if 'user' not in session:
        flash("User is not logged in")
        return redirect("/")
        
    else:
        session.pop('user')
        flash("User is logged out")
        return redirect("/")


#####################################################################



#######################################################################

@app.route("/movies")
def display_movies():
    """ Display three movies on page """

   
    movie_list = []
    i=0

    what_type = request.args.get("type")


    if what_type == "random":

        while i < 3 :
            random_id = random.choice(range(1,45001))
            movie = Movie.query.get(random_id)

            movie_list.append(movie)
            i +=1

    elif what_type == "search":
        genre = request.args.get("genres") 
        decade = request.args.get("decade")
        show_allmovielist = db.session.query(Movie).join(GenresMovies).join(Genre).filter(Genre.gname == genre, Movie.released_at.like('{}%'.format(decade[:3])) ).all()
        print(genre,decade,show_allmovielist)

        for i in range(1,4):
            movie_list.append(random.choice(show_allmovielist))
            show_allmovielist.remove(random.choice(show_allmovielist))



    return render_template("your_movies.html", movies = movie_list)


    
    


##################################################################

@app.route("/pick_movie")
def pick_a_movie():
    """ Showing page where user can pick a movie"""

    return render_template("pick_a_movie.html")


##################################################################






##################################################################


@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    """When user likes something we add to db"""

    movie =  request.form.get('movie_py') 
    print (movie_py)
    print("this is server")

    list_movie = MovieList.query.filter_by(movie_id=movie.movie_id, user_id=session['user'])

    print(list_movie)
    # movie = Movie.query.filter_by(movie_py=movie_py).one()



    if list_movie == []:
        now = datetime.now()
        date_added = now.strftime('%Y/%m/%d %H:%M:%S')
        new_like = MovieList(session['user'],movie_py, date_added,None, '1', None)
        print (new_like)


    elif list_movie[0].interested == None:
        list_movie[0].interested = 1
        print(movie)
            
    
        

    return "Success"








##################################################################







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')