from flask import render_template, url_for, flash, redirect, request
from stockanalyzer import app, bcrypt, db
from stockanalyzer.forms import RegistrationForm, LoginForm
from stockanalyzer.models import User, Watchlist
from flask_login import login_user, current_user, logout_user, login_required
from stockanalyzer.api_caller import validate_ticker, validate_name, Stock


@app.route("/")
def landing():
    return render_template("landing.html", title = "Landing Page")

@app.route("/home")
def home():
    return render_template("home.html", title="HomePage")

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

#----------------------------------------------------------------------------

@app.route('/get_stock_info', methods = ["POST"])
def get_stock():
    name = request.form['stock_input']
    if validate_ticker(str(name)):
        data = Stock(str(name))
        data.get_stock_info()
        data.get_stocks_similars()
        ret = data.fundemental_analysis()
        return render_template("home.html", title="HomePage", verified = "yes", stock_info = data.stock_info, ind_avg = data.industry_averages, analysis = ret)
 
    else: 
        ret_val = validate_name(str(name))
        if (ret_val == -1):      
            return render_template("home.html", stocks_info="Please enter a valid name or symbol", title="HomePage")
        else:
            data = Stock(ret_val)
            data.get_stock_info()
            data.get_stocks_similars()
            ret = data.fundemental_analysis()
            return render_template("home.html", title="HomePage", verified = "yes", stock_info = data.stock_info, ind_avg = data.industry_averages, analysis = ret)
    
