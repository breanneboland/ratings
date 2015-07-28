"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

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
    
    email = request.form.get("email")
    password = request.form.get("password")

    if email in User.query.all():
        #flash message logged-in
        #put in session
        flash("You're logged in! Great!")
        session['email'] = email
        return redirect('/')
    else:
        #flash message - we created an account for you & logged you in
        #put in session
        #put in DB
        flash("We created an account for you with given email and pw - and you're logged in! Oh yeah!")

        session['email'] = email

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')
        #Logs you in, but there's some sort of error happening. Unsure if it actually commits to DB. 
        #Next on the list after that: log out and redirect to the user's details page

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()