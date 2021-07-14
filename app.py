from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '80942c0114beea680cce7e5e2220663f'
ratios = [{"pe":20, "eps":30, "working_ratio":4}, {"pe":30, "eps":10, "working_ratio":1}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", stocks_info=ratios, title="HomePages")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect (url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash("Unsuccessful login. Please check username and password", 'danger')
    return render_template('login.html', title='LogIn', form=form)

if __name__ == "__main__":
    app.run(debug = True)