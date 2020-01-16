from flask import render_template, flash, redirect, url_for
from studentapp import app
from studentapp.forms import LoginForm
from studentapp.models import User
from flask_login import current_user, login_user, logout_user


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home", user=None)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            # load user
            login_user(user)
            return redirect(url_for("index"))
        flash(f"Invalid username or password provided")
        return redirect(url_for("login"))
    return render_template("login.html", form=form, title="Log In")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    return render_template("admin.html", title="Admin")