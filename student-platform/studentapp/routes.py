from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from studentapp import app, db
from studentapp.forms import LoginForm, AddUserForm
from studentapp.models import User
from flask_login import current_user, login_user, logout_user, login_required


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f"Invalid username or password provided")
            return redirect(url_for("login"))
        # load user
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc == "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form, title="Log In")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html", title="Admin")


@app.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password_hash(form.password.data)
        user.role = form.roles.data
        db.session.add(user)
        db.session.commit()
        flash(f"{user.username} user added")
        return redirect(url_for("add_user")) # redirect used to clear form
    return render_template("add_user.html", title="Add User", form=form)