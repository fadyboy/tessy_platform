from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from studentapp.models import Role, User, Classroom


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

# Helper function for the query_factory param
def roles_query():
    return Role.query

# Helper function to resolve Value error for QuerySelectField
def get_pk(obj):
    return str(obj)


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    roles = QuerySelectField(query_factory=roles_query, allow_blank=True, get_label="name", get_pk=get_pk,
                             validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already exists! Please use another username")

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email is not None:
            raise ValidationError("Email already exists! Please enter another email")


class AddStaffForm(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired()])
    middlename = StringField("Middlename")
    surname = StringField("Surname", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("", ""), ("Male", "Male"), ("Female", "Female")],
                         validators=[DataRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[DataRequired()])
    contact_number = StringField("Contact number")
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


def classroom_query():
    return Classroom.query


class AddStudentForm(AddStaffForm):
    contact_number = StringField("Parent/Guardian Contact Number")
    email = StringField("Parent/Guardian Email", validators=[DataRequired(), Email()])
    parent_guardian_name = StringField("Parent/Guardian name")
    classrooms = QuerySelectField(query_factory=classroom_query, allow_blank=True, blank_text="Select class",
                                  get_label="classroom_symbol", get_pk=get_pk)
    submit = SubmitField("Submit")







