"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
import datetime
import calendar

def load_users():
    """Load users from u.user into database."""
    file_open = open("seed_data/u.user")
    # file_data = file_open.read()
 
    for line in file_open:
        temp_data = line.rstrip()
        split_data = temp_data.split("|")
        # Did not include email and password as users would add that later
        user_id_value = split_data[0]
        age_value = split_data[1]
        zipcode_value = split_data[4]
        temp_user_object = User(user_id = user_id_value, age = age_value, zipcode = zipcode_value)
        db.session.add(temp_user_object)
        db.session.commit()

    print "You did it!"
   

# Original file structure: |- separated list of: user id | age | gender | occupation | zip code

def load_movies():
    """Load movies from u.item into database."""

    file_open = open("seed_data/u.item")

    for line in file_open:
        temp_data = line.rstrip()
        split_data = temp_data.split("|")
        movie_id_value = split_data[0]
        title_value = split_data[1]
        title_value = title_value[:-7]
        print title_value
        release_date_value = split_data[2]
        release_date_value = (release_date_value).strip("-")

        date_text = "13SEP2014"
        date = datetime.datetime.strptime(date_text, "%d%b%Y")

        print(date)
        print(calendar.timegm(date.utctimetuple()))



        imdb_url_value = split_data[4]
        temp_item_object = Movie(movie_id = movie_id_value, title = title_value, release_date = release_date_value, imdb_url = imdb_url_value)
        db.session.add(temp_item_object)
        db.session.commit()     

    print "Movies happened!"   

#current mystery: strptime is not in datetime? How do we call it? Importing datetime is not enough. 
#Format for our date: "%d %b %Y"
#maybe start here: https://docs.python.org/2/library/datetime.html

# movie id | movie title | release date | video release date | IMDb URL |
# Item
# movie_id: INT, shared with Data table, unique primary key
# title: VARCHAR(60), NOT NULL
# release date: INT, NOT NULL
# IMDB URL: VARCHAR(150)

def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
