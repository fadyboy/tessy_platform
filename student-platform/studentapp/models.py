from studentapp import db


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(16))

    def __repr__(self):
        return f"User: {self.username}"


class Person(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    middlename = db.Column(db.String(64))
    surname = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(16))
    date_of_birth = db.Column(db.DateTime)
    contact_number = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)


class Staff(Person):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)



class Student(Person):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    parent_guardian_name = db.Column(db.String(128))
    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"))


class Classroom(db.Model):
    __tablename__ = "classroom"
    id = db.Column(db.Integer, primary_key=True)
    classroom_name = db.Column(db.String(128))
    classroom_symbol = db.Column(db.String(8))
    students = db.relationship("Student", backref="classroom", lazy="dynamic")