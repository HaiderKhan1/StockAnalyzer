from flask import render_template, url_for, flash, redirect
from stockanalyzer import app, bcrypt, db
from stockanalyzer.forms import RegistrationForm, LoginForm
from stockanalyzer.models import User, Watchlist
from flask_login import login_user, current_user, logout_user, login_required


ratios = [{"pe":20, "eps":30, "working_ratio":4}, {"pe":30, "eps":10, "working_ratio":1}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", stocks_info=ratios, title="HomePages")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, isAdmin=0, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect (url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash("Unsuccessful login. Please check email and password", 'danger')
    return render_template('login.html', title='LogIn', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
   
