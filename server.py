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
def logs_you_in(user_id):
    """Redirects the user after they've logged in"""
    
    email_value = request.form.get("email")
    password = request.form.get("password")
    user_query = User.query.filter_by(email = email_value).first()
    #Queries the User db to see if there's an email equal to the input from the user
    print user_query
    # print user_query.password

    if user_query == None:
        flash("We created an account for you with given email and pw - and you're logged in! Oh yeah!")

        session['email'] = email_value

        new_user = User(email=email_value, password=password)
        db.session.add(new_user)
        db.session.commit()
    else:
        if user_query.password == password:
            flash("You're logged in! Great!")
            session['email'] = email_value
        else: 
            flash("Password and login don't match. Try again!")
            return render_template('login.html')
    
    user_id = user_query.user_id
    return redirect('/user/<int:user_id>')

#Need to make the user information page. Need to nail down the finer points of the URL above this line.
#(Establishing variable, making sure it's passed, inheritance, etc.) Basically, start at User Details.
#Then onto Movie List.

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