from studentapp import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from studentapp.utils import avatar


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64, collation="NOCASE"), index=True, unique=True)
    email = db.Column(db.String(128, collation="NOCASE"), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, nullable=False, server_default="t")
    role = db.relationship("Role", secondary="user_roles", uselist=False)

    def __repr__(self):
        return f"User: {self.username}"

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_avatar(self, size):
        return avatar(self.email, size)


class Person(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(32), nullable=False, unique=True)
    firstname = db.Column(db.String(64), nullable=False)
    middlename = db.Column(db.String(64))
    surname = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(16))
    birthday = db.Column(db.DateTime)
    contact_number = db.Column(db.String(128))
    email = db.Column(db.String(128))
    #TODO: Add contact address field?

    def __repr__(self):
        return f"{self.firstname} {self.surname}"

    def get_person_avatar(self, size):
        return avatar(self.email, size)

    def format_birthday(self):
        formatted_birthday = self.birthday.strftime("%d %B %Y")
        return formatted_birthday


class Staff(Person):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)


class Student(Person):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    parent_guardian_name = db.Column(db.String(128))
    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"), nullable=False)

    def display_classroom_symbol(self):
        classroom = Classroom.query.get(self.classroom_id)
        return classroom.classroom_symbol


class Classroom(db.Model):
    __tablename__ = "classroom"
    id = db.Column(db.Integer, primary_key=True)
    classroom_name = db.Column(db.String(128), nullable=False)
    classroom_symbol = db.Column(db.String(8), nullable=False, unique=True)
    students = db.relationship("Student", backref="classroom", lazy="dynamic")

    def __repr__(self):
        return f"Classroom: {self.classroom_symbol}"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return f"Role: {self.name}"


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    code = db.Column(db.String(16), unique=True, index=True)

    def __repr__(self):
        return f"Subject: {self.name}"


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))

