"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime

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
        release_date_value = split_data[2]

        #Checks for movies with no release date, which otherwise throw an error
        if release_date_value == "":
            continue
        else:
            release_date_value = datetime.strptime(release_date_value, "%d-%b-%Y")
        
        imdb_url_value = split_data[4]

        temp_item_object = Movie(movie_id = movie_id_value, title = title_value, release_date = release_date_value, imdb_url = imdb_url_value)
        db.session.add(temp_item_object)
    
    db.session.commit()     

    print "Movies happened!"   

def load_ratings():
    """Load ratings from u.data into database."""

    file_open = open("seed_data/u.data")

    for line in file_open:
        temp_data = line.rstrip()
        split_data = temp_data.split("\t")
        user_id_value = split_data[0]
        movie_id_value = split_data[1]
        score_value = split_data[2]

        temp_rating_object = Rating(user_id = user_id_value, movie_id = movie_id_value, score = score_value)
        db.session.add(temp_rating_object)

    db.session.commit()

    print "We have ratings, yeah!"

#user_id \t movie_id \t score \t timestamp
#We only want the first three

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
