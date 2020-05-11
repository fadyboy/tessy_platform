from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField,\
    PasswordField
from wtforms.fields.html5 import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,\
    Length
from flask_wtf.file import FileRequired, FileField
from studentapp.models import Role, User, Classroom, Subject, Staff, Student,\
    Sessions


# Helper function to resolve the Value error for the QuerySelectField
def get_pk(obj):
    return str(obj)


# Helper function for query_factory in roles dropdown field
def roles_query():
    return Role.query


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6,
                                                            message="Password must have at \
                                        least 6 characters")])
    password2 = PasswordField("Repeat Password",
                              validators=[DataRequired(),
                                          EqualTo("password",
                                                  message="Passwords must \
                                                      match"
                                                  )])
    roles = QuerySelectField(query_factory=roles_query, allow_blank=True,
                             get_label="name", get_pk=get_pk,
                             validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                f"Username - {username.data} \
                already exists! Please use another username"
            )

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email is not None:
            raise ValidationError(
                f"Email -{email.data} already exists! Please \
                enter another email")
