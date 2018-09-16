from jinja2 import StrictUndefined

import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Movie, MovieList, connect_to_db, db

import requests

from imdb import IMDb

import random

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
    print(username + '1')

    QUERY = """
        SELECT username
        FROM users
        WHERE username = :username
        """

    db_cursor = db.session.execute(QUERY, {'username': username})
    row = db_cursor.fetchone()
    print(row + '2')

    return row


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
    print(row)

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

@app.route("/movies")
def display_movies():
    """ Store and then displaying selection of 3 movies"""


    movie_list = get_random_movies(3)
    show_movies = []

    while len(show_movies) < 3:

        for movie in movie_list:

            if 'cover url' in movie.keys():


                title = movie['title']
                released_at = movie['year']
                poster = movie['cover url']



                QUERY = """
                    INSERT INTO movies (title, released_at, poster)
                    VALUES (:title, :released_at, :poster)
                    """

                db_cursor = db.session.execute(QUERY, {'title': title, 
                                'released_at': released_at,  'poster':poster})


                db.session.commit()
                show_movies.append(movie)


            else:
                another_movie = get_random_movies(1)
                movie_list.append(another_movie[0])


    return render_template("your_movies.html", movies = show_movies)    


    
    


def get_random_movies(num_random):
    """ Returns a list with 3 random movies"""

    i=0
    movie_list = []

    ia = IMDb()


    while i < num_random :
        random_id = random.choice(range(1,200000))
        movie = ia.get_movie(random_id)
        movie_list.append(movie)
        i +=1

    print(movie_list)
    print("get_random done")
    return movie_list










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