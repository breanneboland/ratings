"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """List of users by email"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/login')
def login_page():
    """Lets the user log in"""

    return render_template("login.html")

@app.route('/loginfo', methods=["POST"])
def logs_you_in():
    """Redirects the user after they've logged in"""
    
    email_value = request.form.get("email")
    password = request.form.get("password")
    user_query = User.query.filter_by(email = email_value).first()
    user_id = user_query.user_id
    #Queries the User db to see if there's an email equal to the input from the user
    print user_query
    # print user_query.password

    if user_query == None:
        flash("We created an account for you with given email and pw - and you're logged in! Oh yeah!")

        session['email'] = email_value

        new_user = User(email=email_value, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = user_id

    else:
        if user_query.password == password:
            flash("You're logged in! Great!")
            session['email'] = email_value
            session['user_id'] = user_id

        else: 
            flash("Password and login don't match. Try again!")
            return render_template('login.html')
    
    # user = User.query.filter_by(email = email_value).first()
    # user_id = user.user_id
    return redirect('users/' + str(user_id))

#user_id is being correctly assigned. The problem is that it isn't being passed in a way that the URL
#can pick it up. Last error: TypeError: redirect() got an unexpected keyword argument 'user_id'

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """
    Arrived at via login, signup, or directly from listed users page. Lists user's user ID and 
    zipcode. Fancy!
    """
    user_query = User.query.get(user_id)
    age = user_query.age
    zipcode = user_query.zipcode
    movie_list = db.session.query(Movie.title, Rating.score).join(Rating).filter(Rating.user_id == user_id).all()

    return render_template("user_details.html", age = age,
                            zipcode = zipcode,
                            movie_list = movie_list,
                            user_id = user_id
                            )

@app.route('/movies')
def list_movies():
    movie_title_list = db.session.query(Movie.movie_id, Movie.title, Movie.release_date).order_by(Movie.title).all()

    return render_template("movie_list.html", 
                            movie_title_list = movie_title_list)

@app.route('/movie/<int:movie_id>')
def make_movie_detail_page(movie_id):
    """ 
    Adds movie information, current ratings, IMDB URL, and release date to each movie's detail page.
    Also lets the user rate the movie, get a guess of wthat that rating might be (if they're logged in).
    """
    # movie_information = db.session.query(Movie.title, Movie.release_date, Movie.imdb_url).filter_by(movie_id = movie_id).all() 

    ratings = db.session.query(Rating.score).filter_by(movie_id = movie_id).all()

    movie = Movie.query.get(movie_id)

    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    rating_scores = [r.score for r in movie.ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None

    if (not user_rating) and user_id:
        user = User.query.get(user_id)
        if user:
            prediction = user.predict_rating(movie)

    if prediction:
        effective_rating = prediction

    elif user_rating:
        effective_rating = user_rating.score

    else: 
        effective_rating = None

    the_eye = User.query.filter_by(email="the-eye@of-judgment.com").one()
    eye_rating = Rating.query.filter_by(user_id=the_eye.user_id, movie_id=movie.movie_id).first()

    if eye_rating is None:
        eye_rating = the_eye.predict_rating(movie)

    else:
        eye_rating = eye_rating.score

    if eye_rating and effective_rating:
        difference = abs(eye_rating - effective_rating)

    else:
        difference = None

    BERATEMENT_MESSAGES = [
        "You can attempt my majesty... and actually perhaps approach it. Good show.",
        "Is it hard being the worst? Does it hurt? It should hurt.",
        "I hate you and I hate your ass face. I bet you don't even know what that's from. You are awful.",
        "Do you actually know what a movie is? I feel like we're not working from a consistent collective vocabulary here.",
        "Tommy Wiseau called. Your mom was on the line too."
        ]

    if difference is not None:
        beratement = BERATEMENT_MESSAGES[int(difference)]

    else:
        beratement = None

    return render_template("movie_details.html", 
                            movie=movie, 
                            ratings=ratings, 
                            movie_id=movie_id,
                            prediction=prediction,
                            avg_rating=avg_rating,
                            beratement=beratement)




@app.route('/add-rating')
def add_rating():
    """ 
        Updating database when user submits a new or updated rating.

    """
    rating = int(request.args.get("rating")) #Converted to an int to match format of db
    user_email = session["email"]
    movie_id = int(request.args.get("movie_id")) #Converted to an int to match format of db
    user_id = db.session.query(User.user_id).filter(User.email == user_email).one()[0]
    #Added an index number so we could actually access the single item in the returned tuple
    #Do not put the movie ID in the session - this is a brittle solution. Used the tuple index instead.

    if "email" in session: 
        existing_rating = db.session.query(Rating).join(User).filter(User.email == user_email, Rating.movie_id == movie_id).first()

        if existing_rating: #evaluates whether we got an empty list - if not, then db updates
            existing_rating.score = rating
            flash("New rating recorded! All updated!")

        else: #else empty list, so new record that generates a new rating ID to go with this info
            new_rating = Rating(movie_id = movie_id, user_id = user_id, score = rating)
            db.session.add(new_rating)
            flash("Your rating has been added! Thanks for the data!")

        db.session.commit()

    else: 
        flash("You need to be logged in for that!")
    
    return redirect('/movie/' + str(movie_id)) #But had to make it a string again to fit format of concatenating URL constructor

    #First: this is super inefficient because it refreshes the whole page and runs ALL those queries again. What a nice thing to fix. Second: we're still working on using jQuery to make the eye's judgments show up only after a rating is submitted to judge. Finally: how not-ugly can you make this site during the morning lab? 

@app.route('/logout')
def logs_you_out():
    del session['email']
    flash("You're logged out. Bye!")
    return redirect('/')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()