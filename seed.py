"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app


# open and read a file
# parse a line
# create an object
# add the object to the db.session
# repeat until all objects are added
# commit

def load_users():
    """Load users from u.user into database."""
    file_open = open("seed_data/u.user")
 
    for line in file_open:
        file_line = file_open.readline().rstrip()

        file_data = file_line.split("|")
        print file_data
        
       # user_id_value = row[0]
    #     email_value = None #Will SQLAlchemy interpret this as NULL?
    #     password_value = None
    #     age_value = row[1]
    #     zipcode_value = row[4]
    #     temp_user_object = User(user_id = user_id_value, email=email_value, password = password_value, age = age_value, zipcode = zipcode_value)
    #     db.session.add(temp_user_object)
    #     db.session.commit()

    # for row in processed_data:
    #     print row

    #     

#         jada = User(email="jada@gmail.com", password="abc123", age=25,
# ...     zipcode="94103")

    # user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # email = db.Column(db.String(64), nullable=True)
    # password = db.Column(db.String(64), nullable=True)
    # age = db.Column(db.Integer, nullable=True)
    # zipcode = db.Column(db.String(15), nullable=True)

# a |- separated list of: user id | age | gender | occupation | zip code

def load_movies():
    """Load movies from u.item into database."""


def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
