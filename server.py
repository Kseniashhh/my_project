from jinja2 import StrictUndefined

import os

from flask import Flask

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

from flask import (Flask, render_template, redirect, request, flash,
                   session,jsonify)

from model import User, Movie, MovieList, Genre, GenresMovies, connect_to_db, db

import requests

from imdb import IMDb

import random

import json 

import API_funcs as ap

from datetime import datetime 

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode



# guidebox.api_key = os.environ['GUIDEBOX_TRIAL_KEY']
# guidebox.region = "US"

# API_KEY = os.environ['YELP_API_KEY']

# API_HOST = 'https://api.yelp.com'
# SEARCH_PATH = '/v3/businesses/search'
# BUSINESS_PATH = '/v3/businesses/'
# # DEFAULT_TERM = 'dinner'
# DEFAULT_LOCATION = 'San Francisco, CA' 
# SEARCH_LIMIT = 3


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


@app.route("/user_added.json",methods=['POST'])
def user_signsUp():
    """ Register new user, ignore existing"""

    email = request.form.get("email") 
    pswd = request.form.get("password")
    username = request.form.get("username")
    

    user_exists = if_user_exists(email)

    if user_exists == None:
        add_user(username,email, pswd)
        user_exists = if_user_exists(email)
        session["user"] = user_exists[0]
        session["seen"] = []
        return "True"
    else:  
        return ("This user is aleady registered. Please log in")




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

    user_exists = User.query.filter_by(email=email).first()
    

    if user_exists == None:
        return jsonify(user_exists.serialize())
    elif user_exists.password == pswd:
        session['user'] = user_exists.user_id
        session['seen'] = []
        return jsonify(user_exists.serialize())
    else:
        return jsonify({"ERROR": "Wrong password"})



####################################################################


@app.route("/my_account")
def show_my_account():
    """ Rendering my account"""

    current_user = User.get(user_id = session["user"])

    num_movie = MovieList.query.filter_by(user_id=session,interested=1).count()
    print(num_foods)
    num_foods = 0


    return render_template("my_account.html", user=current_user, mov_count=num_movie, food_count=num_foods)

####################################################################


@app.route("/logout")
def user_logOut():
    """ log out current user """
    
    if 'user' not in session:
        flash("User is not logged in")
        return redirect("/")
        
    else:
        session.pop("user")
        session.pop("seen")
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

    what_type = request.args.get("type")

    mov_list = get_movies(what_type)
    
    return render_template("your_movies.html", movies = mov_list, type=what_type)




def get_movies(what_type):
    """ Get the list of 3 movies"""

    movie_list = []
    i=0


    if what_type == "random":

        while i < 3 :
            random_id = random.choice(range(1,45001))
            movie = Movie.query.get(random_id)
            if movie.movie_id in session["seen"]:
                continue
            else:
                movie_list.append(movie)
                session["seen"].append(movie.movie_id)
                i +=1

    elif what_type == "search":
        genre = request.args.get("genres") 
        decade = request.args.get("decade")
        show_allmovielist = db.session.query(Movie).join(GenresMovies).join(Genre).filter(Genre.gname == genre, Movie.released_at.like('{}%'.format(decade[:3])),).all()
#add to the filter
        while i < 3 :
            mov = random.choice(show_allmovielist)
            if mov.movie_id in session["seen"]:
                show_allmovielist.remove(random.choice(show_allmovielist))
                continue
            else:
                movie_list.append(mov)
                session["seen"].append(mov.movie_id)
                show_allmovielist.remove(random.choice(show_allmovielist))
                i +=1



    return movie_list


##################################################################

@app.route("/more_movies.json")
def show_more():
    """ Show more movies when user clicks on more"""

    what_type = request.args.get("type")
    # what_decade = request.args.get("decade")
    # what_genre = request.args.get("genre")


    print(what_type)

    movielist = get_movies(what_type)
    print(movielist)
    serialized_lst = []
    for movie in movielist:
        serialized_lst.append(movie.mov_serial())

    return jsonify({"data": render_template("more.html", movies=serialized_lst,type=what_type)})



##################################################################

@app.route("/foods")
def display_food():
    """ Display three food places on page """

    what_type = request.args.get("type")

    mov_list = get_food(what_type)
    
    return render_template("your_food.html", foods = food_list, type=what_type)




def get_food(what_type):
    """ Get the list of 3 food places"""

    food_list = []
    i=0


    if what_type == "random":

        while i < 3 :
            random_id = random.choice(range(1,45001))
            movie = Movie.query.get(random_id)
            if movie.movie_id in session["seen"]:
                continue
            else:
                movie_list.append(movie)
                session["seen"].append(movie.movie_id)
                i +=1

    elif what_type == "search":
        cuisine = request.args.get("cuisine") 
        price = request.args.get("price")
        show_allmovielist = db.session.query(Movie).join(GenresMovies).join(Genre).filter(Genre.gname == genre, Movie.released_at.like('{}%'.format(decade[:3])),).all()
#add to the filter
        while i < 3 :
            mov = random.choice(show_allmovielist)
            if mov.movie_id in session["seen"]:
                show_allmovielist.remove(random.choice(show_allmovielist))
                continue
            else:
                movie_list.append(mov)
                session["seen"].append(mov.movie_id)
                show_allmovielist.remove(random.choice(show_allmovielist))
                i +=1



    return movie_list



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


@app.route("/add_to_wishlist", methods=["POST"])
def add_to_wishlist():
    """When user likes something we add to db"""

    movie =  request.form.get("movie_id") 
    
    list_movie = MovieList.query.filter_by(movie_id=movie, user_id=session["user"]).all()



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


###################################################################

@app.route("/remove_item", methods=['POST'])
def remove_from_wishlist():
    """Removing item from wishlist"""
    mov_id = request.form.get("movie")

    update_mov = MovieList.query.filter_by(user_id = session['user'],movie_id = mov_id).update(dict(interested = 0))
    db.session.commit()
    
    return "Success. "




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