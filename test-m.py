from flask import session
from models import db, connect_db, User
from app import app

# db.drop_all()
# db.create_all()


# stevan = User.register(username="stevang", password="podop", email='stevangrubac123@gmail.com', firstn="stevan", lastn = "grubac")
# db.session.add(stevan)
# db.session.commit()

print(User.authenticate(username='stevang', pwd='podop'))