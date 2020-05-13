from studentapp.auth import bp
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from studentapp.auth.forms import LoginForm, ResetPasswordRequestForm,\
     ResetPasswordForm
from studentapp.models import User
from werkzeug.urls import url_parse
from studentapp.auth.email import send_password_reset_email
from studentapp import db


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None and user.check_password(form.password.data):
            flash("Invalid username or password provided")
            return redirect(url_for("auth.login"))  # login function
        # load user
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc == "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", form=form, title="Log In")


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for instructions to reset your password")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html",
                           title="Reset Password Request", form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html",
                           form=form, title="Reset Password")
