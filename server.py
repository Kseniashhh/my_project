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

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode



# guidebox.api_key = os.environ['GUIDEBOX_TRIAL_KEY']
# guidebox.region = "US"

API_KEY = os.environ['YELP_API_KEY']

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA' 
SEARCH_LIMIT = 3


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


@app.route("/user_added",methods=['POST'])
def user_signsUp():
    """ Register new user, ignore existing"""

    email = request.form.get("email") 
    pswd = request.form.get("password")
    username = request.form.get("username")
    

    user_exists = if_user_exists(email)

    if user_exists == None:
        add_user(username,email, pswd)
        print("user doesn't exist")
        user_exists = if_user_exists(email)
        session['user'] = user_exists[0]
        # return redirect("/")
        return "True"
    else:  
        return ("This user is aleady registered. Please log in")
        # return redirect("/login")




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

@app.route("/login_user.json", methods=['POST'])
def user_login():
    """ Logs user in """

    email = request.form.get("email") 
    pswd = request.form.get("password")

    user_exists = User.query.filter_by(email=email, password=pswd).all()


    if user_exists == None:
        return jsonify('False')
    else:  
        session['user'] = user_exists[0]
        return jsonify('True')

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


@app.route("/wishlist")
def display_wishlist():
    """ Show movies that user liked"""

    wishlist_list = db.session.query(Movie).join(MovieList).filter(MovieList.user_id == session['user'], MovieList.interested == True).all()
    print (wishlist_list)

    return render_template("wishlist.html", wish_list=wishlist_list)


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

        for i in range(1,4):
            movie_list.append(random.choice(show_allmovielist))
            show_allmovielist.remove(random.choice(show_allmovielist))



    return render_template("your_movies.html", movies = movie_list)


##################################################################

@app.route("/foods")
def display_food():
    """ Display three places on page """

   
    food_list = []
    i=0

    what_type = request.args.get("type")


    if what_type == "random":

        while i < 3 :
            random_id = random.choice(range(1,45001))
            food_path = BUSINESS_PATH + random_id
            food_request = request(API_HOST, business_path, API_KEY)
            print (food_request)

            movie_list.append(food_request)
            i +=1

    elif what_type == "search":
        food_type = request.args.get("type") 
        zipcode = request.args.get("zipcode")
        response = search(API_KEY,)

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

@app.route("/pick_food")
def pick_a_restarant():
    """ Showing page where user can pick a restaurant"""

    return render_template("pick_food.html")





##################################################################


@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    """When user likes something we add to db"""

    movie =  request.form.get('movie_id') 
    
    list_movie = MovieList.query.filter_by(movie_id=movie, user_id=session['user']).all()



    if list_movie == []:
        now = datetime.now()
        date_added = now.strftime('%Y/%m/%d %H:%M:%S')
        new_like = MovieList(user_id = session['user'],movie_id = movie, date_added = date_added,
            rated_at = None, interested = 1, recommended = None)
        db.session.add(new_like)


    elif list_movie[0].interested == None:
        list_movie[0].interested = 1
            
    
    db.session.commit()
  

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