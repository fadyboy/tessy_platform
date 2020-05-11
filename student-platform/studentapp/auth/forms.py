from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(
                            message="Please enter email"),
                            Email(message="Please enter valid email")
                        ]
                        )
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[DataRequired(
            message="Password must contain minimum 6 \
                                     characters"
        ),
            Length(min=6)
        ]
    )
    password2 = PasswordField(
        "Repeat Password",
        validators=[DataRequired(),
                    EqualTo(password,
                            message="Passwords must \
                                                      match"
                            )
                    ])
    submit = SubmitField("Reset Password")
