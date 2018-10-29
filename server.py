from jinja2 import StrictUndefined
import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from flask import (Flask, render_template, redirect, request, flash,
                   session,jsonify)
from model import User, Movie, MovieList, Genre, GenresMovies, FoodList, Food, connect_to_db, db
import requests
from imdb import IMDb
import random
import json 
import API_funcs as ap
from datetime import datetime 
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

from sqlalchemy import func



# guidebox.api_key = os.environ['GUIDEBOX_TRIAL_KEY']
# guidebox.region = "US"

API_KEY = os.environ['YELP_API_KEY']

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DEFAULT_TERM = 'food'
DEFAULT_LOCATION = 'San Francisco, CA' 
SEARCH_LIMIT = 1


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

@app.route('/username_check')
def if_username_exists():
    """ Checks if username is taken """

    username = request.args.get("username")

    QUERY = """
        SELECT username
        FROM users
        WHERE username = :username
        """                                 # rewrite as SQL Alchemy

    db_cursor = db.session.execute(QUERY, {'username': username})
    row = db_cursor.fetchone()

    if row:
        user_name = row[0]
    else:
        user_name = "None"


    return user_name


#####################################################################


@app.route("/user_added.json",methods=['POST'])
def user_signs_Up():
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
        session['food_seen'] = []

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
        session['food_seen'] = []
        return jsonify(user_exists.serialize())
    else:
        return jsonify({"ERROR": "Wrong password"})



####################################################################


@app.route("/mov_chart.json")
def likes_data():
    """Return data about liked content."""


    results_count = db.session.query(Genre.gname, func.count(MovieList.interested)).join(GenresMovies).join(Movie).\
                    join(MovieList).filter(MovieList.user_id==session["user"],MovieList.interested==True).group_by(Genre.gname).all()


    print(results_count)
    user_genres = []
    genre_count = []

    for genre,count in results_count:
        user_genres.append(genre)
        genre_count.append(count)

    print(user_genres)
    print(genre_count)

    color_list=["#BC70A4", "#EADEDB","#6B5B95","#DBB1CD","#EC9787","#BE9EC9","#7F4145","#F3D6E4","#DAA990"]

    need_cols = color_list[:len(user_genres)]



    data_dict = {
                "labels": user_genres,
                "datasets": [
                    {
                        "data": genre_count,
                        "backgroundColor": need_cols,
                        "hoverBackgroundColor": need_cols
                    }]
            }
    return jsonify(data_dict)




######################################################################################


@app.route("/food_chart.json")
def likes_data_food():
    """Return data about liked content."""


    results_count = db.session.query(Food.term, func.count(FoodList.interested)).join(FoodList).\
                    filter(FoodList.user_id==session["user"],FoodList.interested==True).group_by(Food.term).all()


    user_terms = []
    term_count = []

    for food,count in results_count:
        user_terms.append(food)
        term_count.append(count)

   

    color_list=["#B5D279", "#85D68B","#39AC82","#75C653","#9FDFD2","#85AFD6","#75D1C0","#7CA437","#6E3DB8"]

    need_cols = color_list[:len(user_terms)]



    data_dict = {
                "labels": user_terms,
                "datasets": [
                    {
                        "data": term_count,
                        "backgroundColor": need_cols,
                        "hoverBackgroundColor": need_cols
                    }]
            }
    return jsonify(data_dict)




######################################################################################

@app.route('/info_check')
def if_username_email_exists():
    """ Checks if username and email are taken """

    username = request.args.get("username")
    email = request.args.get("email")

    print(username,'+', email)



    username_exists = User.query.filter_by(username=username).first()

    email_exists = User.query.filter_by(email=email).first()

    if (username_exists != None and email_exists != None):
        return "This username and email already registered"
    elif username_exists != None:
        return "This username is already taken"
    elif email_exists != None:
        return "This email is already registered"
    else:
        current_user = User.query.get(session["user"])
        current_user.username = username
        current_user.email = email
        db.session.commit()

        return "Success"



######################################################################################

@app.route("/psw_check", methods=['POST'])
def psw_check():
    """ Checks if current psw matches the one in db """

    pswd = request.form.get("psw")

    print(pswd)

    current_user = User.query.get(session["user"])

    if current_user.password == pswd:
        return "Success"
        # return jsonify(msg="Success")
        # {'msg': 'success'}
    else:
        return "Wrong"

    


######################################################################################


@app.route("/psw_update", methods=['POST'])
def psw_update():
    """ Logs user in """

    pswd = request.form.get("psw")

    print(pswd)

    current_user = User.query.get(session["user"])

    current_user.password = pswd

    db.session.commit()

    return 'Success'


    

    # if user_exists == None:
    #     return jsonify(user_exists.serialize())
    # elif user_exists.password == pswd:
    #     session['user'] = user_exists.user_id
    #     session['seen'] = []
    #     session['food_seen'] = []
    #     return jsonify(user_exists.serialize())
    # else:
    #     return jsonify({"ERROR": "Wrong password"})


######################################################################################


@app.route("/my_account")
def show_my_account():
    """ Rendering my account"""




    current_user = User.query.get(session["user"])



    return render_template("my_account.html", user=current_user)

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

    wishlist_movies = db.session.query(Movie).join(MovieList).filter(MovieList.user_id == session['user'], MovieList.interested == True).all()
    wishlist_foods = db.session.query(Food).join(FoodList).filter(FoodList.user_id == session['user'], FoodList.interested == True).all()

    # print (wishlist_movies)


    return render_template("wishlist_new.html", liked_movies=wishlist_movies, liked_foods=wishlist_foods)


#######################################################################

@app.route("/movies")
def display_movies():
    """ Display three movies on page """

    what_type = request.args.get("type")

    genre = request.args.get("genre") 
    decade = request.args.get("decade")



    mov_list = get_movies(what_type,genre,decade)

    
    return render_template("your_movies.html", movies = mov_list, type=what_type, genre=genre, decade=decade)




def get_movies(what_type,genre=None, decade=None):
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
        
        filtered_movielist = db.session.query(Movie).join(GenresMovies).join(Genre).filter(Genre.gname == genre, Movie.released_at.like('{}%'.format(decade[:3])))
        count_list = filtered_movielist.count()
        remember_num = []

        while i < 3:
            mov_num = random.choice(range(1, count_list))
            if mov_num not in remember_num:
                mov = filtered_movielist.offset(mov_num).first()
                remember_num.append(mov_num)
                session["seen"].append(mov.movie_id)

                movie_list.append(mov)
                i +=1


    return movie_list


##################################################################

@app.route("/more_movies.json")
def show_more():
    """ Show more movies when user clicks on more"""

    what_type = request.args.get("type")
    decade = request.args.get("decade")
    genre = request.args.get("genre")



    movielist = get_movies(what_type,genre, decade)
    serialized_lst = []
    for movie in movielist:
        serialized_lst.append(movie.mov_serial())


    return jsonify({"data": render_template("more.html", movies=serialized_lst,type=what_type,genre=genre, decade=decade)})



##################################################################

@app.route("/foods")
def display_food():
    """ Display three food places on page """

    what_type = request.args.get("type")
    what_term = request.args.get("cuisine")
    what_price = request.args.get("price")


    food_list = get_food(what_type,what_term,what_price)

    # print("food list is ", food_list)

    return render_template("your_food.html", foods = food_list, type=what_type, term=what_term,price=what_price)






def get_food(what_type,what_term=None, what_price=None):
    """ Function that returms list of foods"""
    i=0
    food_list =[]

    

    if what_type == 'random':

        while i < 3 :
            random_off = random.choice(range(1,1001))
            food_choice = ap.search_random(API_KEY, DEFAULT_LOCATION,DEFAULT_TERM, random_off)
            # print(food_choice)
            # print('\n'+ food_choice['businesses'][0]['id'])
            if food_choice['businesses'][0]['id'] in session["food_seen"]:
                continue
            else:
                food_list.append(food_choice['businesses'][0])
                session["food_seen"].append(food_choice['businesses'][0]['id'])
                i +=1



    else:
        
        # print("searching by price ", what_price)
        while i < 3 :
            # random_off = random.choice(range(1,1001))
            food_choice = ap.search(API_KEY, DEFAULT_LOCATION,what_term,what_price)
            print(len(food_choice['businesses']))
            random_off = random.choice(range(1,len(food_choice['businesses'])))
            print(random_off)
            # print(food_choice['businesses'])
            # print('\n'+ food_choice['businesses'][random_off]['id'] + '\n')
            
            if food_choice['businesses'][random_off]['id'] in session["food_seen"]:
                continue
            else:
                food_list.append(food_choice['businesses'][random_off])
                session["food_seen"].append(food_choice['businesses'][random_off]['id'])
                i +=1
    
    print(food_list)

    print("session: ")
    print(session["food_seen"])

    return food_list



##################################################################

@app.route("/more_food.json")
def show_more_food():
    """ Show more movies when user clicks on more"""

    what_type = request.args.get("type")
    price = request.args.get("price")
    term = request.args.get("cuisine")



    food_list = get_food(what_type,term,price)
   

    return jsonify({"data": render_template("more_food.html", foods=food_list,type=what_type,price=price, term=term)})





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
            interested = 1, shared = None)
        db.session.add(new_like)


    elif list_movie[0].interested == None:
        list_movie[0].interested = 1
            
    
    db.session.commit()
  

    return "Success"


###################################################################

@app.route("/add_to_wishlist_food", methods=["POST"])
def add_to_wishlist_food():
    """When user likes something we add to db"""

    food_id =  request.form.get("food_id") 
    food = ap.get_business(API_KEY,food_id)
    check_food = Food.query.filter_by(yelp_id=food_id).first()
    main_categories = ["Mediterranean", "Chinese", "French", "Italian","American", "Sushi","Thai","Indian"]

    if check_food != None:
        food_list = FoodList.query.filter_by(food_id=check_food.food_id, user_id=session["user"]).all()
        
    else:
        print(food["categories"])
        for alias in food["categories"]:
            if alias["title"] in main_categories:
                term = alias["title"]
                break
            else:
                term = "Other" 
        print(term)

        new_food = Food(yelp_id=food_id, name=food["name"], 
                        term=term,
                        price=food["price"],
                        address = (food["location"]["display_address"][0]+food["location"]["display_address"][1]), 
                        image_url=food["image_url"])
        db.session.add(new_food)
        db.session.commit()
        food_list = FoodList.query.filter_by(food_id=new_food.food_id, user_id=session["user"]).all()
        

    if food_list == []:
        now = datetime.now()
        date_added = now.strftime('%Y/%m/%d %H:%M:%S')
        new_food_like = FoodList(user_id = session['user'],food_id = new_food.food_id, date_added = date_added, 
                            interested = 1, shared = None)
        db.session.add(new_food_like)

    elif food_list:
        if food_list[0].interested == None:
            food_list[0].interested = 1

    
    db.session.commit()
  

    return "Success"


###################################################################

@app.route("/remove_item", methods=['POST'])
def remove_from_wishlist():
    """Removing item from wishlist"""
    content_id = request.form.get("content")
    content_type = ''.join(list(content_id)[:3])
    content_id = ''.join(list(content_id)[3:])

    print(content_id, content_type)

    if content_type == "mov":
        update_mov = MovieList.query.filter_by(user_id = session['user'],movie_id = content_id).update(dict(interested = 0))
        db.session.commit()

        print (MovieList.query.filter_by(user_id = session['user'],movie_id = content_id).first())
    elif content_type == "foo":
        update_foo = FoodList.query.filter_by(user_id = session['user'],food_id = content_id).update(dict(interested = 0))
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