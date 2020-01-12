from studentapp import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(16))

    def __repr__(self):
        return f"User: {self.username}"

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Person(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    middlename = db.Column(db.String(64))
    surname = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(16))
    birthday = db.Column(db.DateTime)
    contact_number = db.Column(db.String(128))
    email = db.Column(db.String(128))

    def __repr__(self):
        return f"Person: {self.firstname} {self.surname}"


class Staff(Person):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)


class Student(Person):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    parent_guardian_name = db.Column(db.String(128))
    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"), nullable=False)


class Classroom(db.Model):
    __tablename__ = "classroom"
    id = db.Column(db.Integer, primary_key=True)
    classroom_name = db.Column(db.String(128))
    classroom_symbol = db.Column(db.String(8))
    students = db.relationship("Student", backref="classroom", lazy="dynamic")

    def __repr__(self):
        return f"Classroom: {self.classroom_symbol}"
