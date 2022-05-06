1- How to run the app :
)- execute pip install -r requirements.txt
)- execute App.py

2- The App structure:
App.py ===> main initialiser for the App
app directory :
authentication fun
main index page

3- Some notes for Mohamed Ali :
the creation of the db tables should be in models.py
example of user table creation in flask with SQLAlchemy

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    //here the methods of the user
    create account 
    ...

4- Some notes for Rami :
the base.html  template should extends {% extends "bootstrap/base.html" %}
details in Bootstrap Integration with Flask-Bootstrap section of the book