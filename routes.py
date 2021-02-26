from flask import render_template, flash, redirect, url_for
from main import app
from main.forms import RegistrationForm, LoginForm
from main.models import User,Post
from main import db, bcrypt
from flask_login import login_user

db.create_all()

posts=[
    {'Author':'Gokul',
     'p':'Lorem Ipsum'},
    {'Author':'Sivadasan',
     'p':'Nice para'}
]
@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template("user.html", user=user)

@app.route('/profile/<name>')
def profile(name):
    return render_template("profile.html", name=name)

@app.route('/blog')
def blog():
    return render_template('post.html', posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password= hash_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You can now login.','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET','POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            return redirect(url_for('blog'))
        else:
            flash('Unsuccessful Login. Please check email and password.','danger')
    return render_template('login.html', form=form, title='Login')
