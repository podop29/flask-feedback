from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__="users"


    username = db.Column(db.String(20), primary_key=True, unique=True)

    password = db.Column(db.String, nullable=False)

    email = db.Column(db.String(50), unique=True )

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)


    @classmethod 
    def register(cls, username, password, email, firstn, lastn):

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username, password=hashed_utf8, email=email, first_name = firstn, last_name = lastn)


    @classmethod
    def authenticate(cls,username,pwd):
        "Validate that user exists and password is correct"

        u= User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

