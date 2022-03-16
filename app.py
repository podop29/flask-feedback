from distutils.log import Log
from flask import Flask, request, render_template, flash, redirect, session
from models import connect_db, db, User
from forms import UserRegisterForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "OOooOOOoOOOoo000"

connect_db(app)


@app.route('/')
def home():
    return redirect('/register')


@app.route('/register', methods=["GET", 'POST'])
def register_user():
    form = UserRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        "Create New User with form data"
        NewUser = User.register(username=username, password=password, email=email,
        firstn=first_name, lastn=last_name)
        "Send to db"
        db.session.add(NewUser)
        db.session.commit()
        session['username'] = NewUser.username
        return redirect(f'/user/{NewUser.username}')
    else:
        return render_template('register.html', form = form)


@app.route("/login", methods=["GET","POST"])
def show_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)
        if user:
            session['username'] = user.username
            return redirect(f'/user/{user.username}')
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)



@app.route('/user/<username>')
def show_secret(username):

    if "username" not in session:
        return redirect('/login')
    
    user = User.query.get(username)
    return render_template("userinfo.html",user=user)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')
