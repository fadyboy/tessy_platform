from studentapp import app
from flask import render_template
from studentapp.email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        "Reset Your Password",
        sender=app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template(
            "auth/password_reset.txt",
            user=user,
            token=token
        ),
        html_body=render_template(
            "auth/reset_password.html",
            user=user,
            token=token
        )
    )
