"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import correlation

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Prints actual useful information about the user instead of its memory location"""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

    def similarity(self, other):
        """ Return Pearson rating for the logged-in user as compard to another user.
        """

        current_user_ratings = {}
        paired_ratings = []

        for rating_object in self.ratings:
            current_user_ratings[rating_object.movie_id] = rating_object

        for other_rating_object in other.ratings:
            user_rating = current_user_ratings.get(other_rating_object.movie_id)
            if user_rating:
                paired_ratings.append((user_rating.score, other_rating_object.score))

        if paired_ratings:
            return correlation.pearson(paired_ratings)

        else: 
            return 0.0

    def predict_rating(self, movie):
        """ Predict a user's rating of a movie using the best match available in the db.
        """

        other_ratings = movie.ratings

        similarities = [
            (self.similarity(rating_object.user), rating_object)
            for rating_object in other_ratings]

        similarities.sort(reverse=True)

        similarities = [(sim_coeff, rating_object) for sim_coeff, rating_object in similarities if sim_coeff > 0]

        if not similarities:
            return None

        numerator = sum([rating_object.score * sim_coeff for sim_coeff, rating_object in similarities])
        denominator = sum([sim_coeff for sim_coeff, rating_object in similarities])

        return numerator / denominator

class Movie(db.Model):
    """table of movie information"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    imdb_url= db.Column(db.String(150), nullable=False)

    def __repr__(self):
        """Prints actual useful information about the movie instead of its memory location"""

        return "<Movie movie_id=%s title=%s release date=%s>" % (self.movie_id, self.title, self.release_date)

class Rating(db.Model):
    """table of user ratings"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))
    movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Prints actual useful information about the ratings instead of its memory location"""

        return "<Rating rating_id=%d movie_id=%d user_id=%s score=%d>" % (self.rating_id, self.movie_id, self.user_id, self.score)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."