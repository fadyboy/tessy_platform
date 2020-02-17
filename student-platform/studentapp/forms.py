from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
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
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6, message="Password must have at least 6 characters")])
    password2 = PasswordField("Repeat Password",
                              validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
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


class EditUserForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6, message="Password must have at least 6 characters")])
    password2 = PasswordField("Repeat Password",
                              validators=[EqualTo("password", message="Passwords must match"), DataRequired()])
    is_active = SelectField("Enable/Disable", choices=[("", ""), ("true", "Enable"), ("false", "Disable")],
                            validators=[DataRequired()])
    roles = QuerySelectField(query_factory=roles_query, allow_blank=True, get_label="name", get_pk=get_pk,
                             validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddStaffForm(FlaskForm):
    serial_number = StringField("Staff Number", validators=[DataRequired()])
    firstname = StringField("Firstname", validators=[DataRequired()])
    middlename = StringField("Middlename")
    surname = StringField("Surname", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("", ""), ("Male", "Male"), ("Female", "Female")],
                         validators=[DataRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[DataRequired()])
    contact_number = StringField("Contact Number")
    email = StringField("Email", validators=[DataRequired(), Email("Please enter valid email")])
    address = StringField("Address")
    submit = SubmitField("Submit")

    def validate_serial_number(self, serial_number):
        serial = Staff.query.filter_by(serial_number=serial_number.data).first()
        if serial is not None:
            raise ValidationError(f"{serial.serial_number} is already in use! Please enter another staff number")


class EditStaffForm(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired(message="Firstname is required")])
    middlename = StringField("Middlename")
    surname = StringField("Surname", validators=[DataRequired(message="Surname is required")])
    contact_number = StringField("Contact Number", validators=[DataRequired(message="Contact Number is required")])
    email = StringField("Email",
                        validators=[Email(message="Enter valid email"), DataRequired(message="Email is required")])
    address = StringField("Address", validators=[DataRequired(message="Address is required")])
    submit = SubmitField("Submit")


# helper function for query factory for classrooms dropdown field
def classroom_query():
    return Classroom.query


class AddStudentForm(AddStaffForm):
    serial_number = StringField("Student Number", validators=[DataRequired()])
    contact_number = StringField("Parent/Guardian Contact Number")
    email = StringField("Parent/Guardian Email", validators=[DataRequired(), Email()])
    parent_guardian_name = StringField("Parent/Guardian name", validators=[DataRequired()])
    address = StringField("Address")
    classrooms = QuerySelectField(query_factory=classroom_query, allow_blank=True, blank_text="Select class",
                                  get_label="classroom_symbol", get_pk=get_pk, validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_serial_number(self, serial_number):
        serial = Student.query.filter_by(serial_number=serial_number.data).first()
        if serial is not None:
            raise ValidationError(f"{serial.serial_number} is already in use! Please enter another student number")


class EditStudentForm(EditStaffForm):
    contact_number = StringField("Parent/Guardian Contact Number", validators=[DataRequired()])
    email = StringField("Parent/Guardian Email", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    classrooms = QuerySelectField(query_factory=classroom_query, allow_blank=True, blank_text="Select class",
                                  get_label="classroom_symbol", get_pk=get_pk,
                                  validators=[DataRequired(message="Please select a class")])


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


class EditSubjectForm(FlaskForm):
    name = StringField("Subject Name")
    code = StringField("Subject Code")
    submit = SubmitField("Submit Change")

