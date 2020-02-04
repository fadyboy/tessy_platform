from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from studentapp.models import Role, User, Classroom, Subject, Staff, Student


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

# Helper function for the query_factory in roles dropdown field
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
            raise ValidationError(f"Username - {username.data} already exists! Please use another username")

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email is not None:
            raise ValidationError(f"Email -{email.data} already exists! Please enter another email")


class AddStaffForm(FlaskForm):
    serial_number = StringField("Staff Number", validators=[DataRequired()])
    firstname = StringField("Firstname", validators=[DataRequired()])
    middlename = StringField("Middlename")
    surname = StringField("Surname", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("", ""), ("Male", "Male"), ("Female", "Female")],
                         validators=[DataRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[DataRequired()])
    contact_number = StringField("Contact number")
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

    def validate_serial_number(self, serial_number):
        serial = Staff.query.filter_by(serial_number=serial_number.data).first()
        if serial is not None:
            raise ValidationError(f"{serial.serial_number} is already in use! Please enter another staff number")


# helper function for query factory for classrooms dropdown field
def classroom_query():
    return Classroom.query


class AddStudentForm(AddStaffForm):
    serial_number = StringField("Student Number", validators=[DataRequired()])
    contact_number = StringField("Parent/Guardian Contact Number")
    email = StringField("Parent/Guardian Email", validators=[DataRequired(), Email()])
    parent_guardian_name = StringField("Parent/Guardian name", validators=[DataRequired()])
    classrooms = QuerySelectField(query_factory=classroom_query, allow_blank=True, blank_text="Select class",
                                  get_label="classroom_symbol", get_pk=get_pk)
    submit = SubmitField("Submit")

    def validate_serial_number(self, serial_number):
        serial = Student.query.filter_by(serial_number=serial_number.data).first()
        if serial is not None:
            raise ValidationError(f"{serial.serial_number} is already in use! Please enter another student number")


class AddClassroomForm(FlaskForm):
    classroom_name = StringField("Classroom Name", validators=[DataRequired()])
    classroom_symbol = StringField("Classroom Symbol", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddSubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired()])
    code = StringField("Subject Code", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_name(self, name):
        subject = Subject.query.filter_by(name=name.data).first()
        if subject is not None:
            raise ValidationError(f"Subject with name - {name} already exists! Please enter different name")

    def validate_code(self, code):
        subject = Subject.query.filter_by(code=code.data).first()
        if subject is not None:
            raise ValidationError(f"Subject with code - {code} already exists! Please enter different code")







