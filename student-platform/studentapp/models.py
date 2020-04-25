import jwt
import inflect
from studentapp import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from studentapp.utils import avatar
from time import time


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64, collation="NOCASE"), index=True,
                         unique=True)
    email = db.Column(db.String(128, collation="NOCASE"), index=True,
                      unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, nullable=False, server_default="t")
    role = db.relationship("Role", secondary="user_roles", uselist=False)
    image_file_name = db.Column(db.String(128))

    def __repr__(self):
        return f"User: {self.username}"

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_avatar(self, size):
        return avatar(self.email, size)

    def get_reset_password_token(self, expires_in=3600):
        return jwt.encode(
            {
                "reset_password": self.id,
                "exp": time() + expires_in
            },
            app.config["SECRET_KEY"],
            algorithm="HS256"
        ).decode("UTF-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )["reset_password"]
        except Exception:
            return
        return User.query.get(id)


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
    address = db.Column(db.String(200))
    image_file_name = db.Column(db.String(128))

    def __repr__(self):
        return f"{self.firstname} {self.surname}"

    def get_person_avatar(self, size):
        return avatar(self.email, size)

    def format_birthday(self):
        formatted_birthday = self.birthday.strftime("%d %B %Y")
        return formatted_birthday

    # TODO: functionality for default pic
    # remove image


class Staff(Person):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)


class Student(Person):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    parent_guardian_name = db.Column(db.String(128))
    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"),
                             nullable=False)

    def display_classroom_symbol(self):
        classroom = Classroom.query.get(self.classroom_id)
        return classroom.classroom_symbol

    def get_total_students_in_class(self):
        classroom = Classroom.query.get(self.classroom_id)
        return classroom.total_students_in_classroom()


class Classroom(db.Model):
    __tablename__ = "classroom"
    id = db.Column(db.Integer, primary_key=True)
    classroom_name = db.Column(db.String(128), nullable=False)
    classroom_symbol = db.Column(db.String(8), nullable=False, unique=True)
    students = db.relationship("Student", backref="classroom", lazy="dynamic")

    def __repr__(self):
        return f"Classroom: {self.classroom_symbol}"

    def total_students_in_classroom(self):
        students_list = [student for student in self.students]
        total_students = len(students_list)
        return total_students


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return f"{self.name}"


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id",
                                                    ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id",
                                                    ondelete="CASCADE"))


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    code = db.Column(db.String(16), unique=True, index=True)

    def __repr__(self):
        return f"Subject: {self.name}"


class Sessions(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(16), unique=True, index=True, nullable=False)
    current_session = db.Column(db.Boolean, nullable=False,
                                server_default='false')

    def __repr__(self):
        return f"Session: {self.session}"

    def set_as_current_session(self, session_id):
        # first check if a session is already set
        old_session = Sessions.query.filter_by(current_session=True).first()
        new_session = Sessions.query.get(session_id)
        if old_session:
            old_session.current_session = False
            new_session.current_session = True
        elif old_session is None:
            new_session.current_session = True


class StudentResults(db.Model):
    __tablename__ = "student_results"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"),
                           nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"),
                             nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"),
                           nullable=False)
    term = db.Column(db.String(32), nullable=False)
    sessions_id = db.Column(db.Integer, db.ForeignKey("sessions.id"),
                            nullable=False)
    ca_score = db.Column(db.Integer, nullable=False)
    exam_score = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer)
    grade = db.Column(db.String(8))
    grade_remark = db.Column(db.String(32))

    def set_total_score(self, ca_score, exam_score):
        return ca_score + exam_score

    def set_grade_and_remark(self, total_score):
        if total_score >= 80 <= 90:
            grade = "A"
            grade_remark = "EXCELLENT"
        elif total_score > 90:
            grade = "A+"
            grade_remark = "DISTINCTION"
        elif total_score >= 75 <= 79:
            grade = "B+"
            grade_remark = "VERY GOOD"
        elif total_score >= 70 <= 74:
            grade = "B"
            grade_remark = "GOOD"
        elif total_score >= 65 <= 69:
            grade = "C+"
            grade_remark = "CREDIT"
        elif total_score >= 55 <= 64:
            grade = "C"
            grade_remark = "CREDIT"
        elif total_score >= 50 <= 54:
            grade = "C-"
            grade_remark = "CREDIT"
        elif total_score >= 45 <= 49:
            grade = "D"
            grade_remark = "PASS"
        elif total_score >= 40 <= 44:
            grade = "E"
            grade_remark = "PASS"
        else:
            grade = "F"
            grade_remark = "FAIL"

        return grade, grade_remark

    @staticmethod
    def calculate_subject_average_score_in_class(subject_id,
                                                 classroom_id, term,
                                                 sessions_id):
        subject_score_average = db.session.query(db.func.avg(
                                                StudentResults.total_score)
                                                ).filter_by(
                                                    subject_id=subject_id,
                                                    classroom_id=classroom_id,
                                                    term=term,
                                                    sessions_id=sessions_id
                                                    ).all()
        # return the first element of the tuple
        return subject_score_average[0][0]

    @staticmethod
    def calculate_score_position_in_subject(
        subject_id, classroom_id, term, sessions_id,
        student_total_score
    ):
        subject_total_scores_query = db.session.query(
            StudentResults.total_score
        ).filter_by(
            subject_id=subject_id,
            classroom_id=classroom_id,
            term=term,
            sessions_id=sessions_id
        ).order_by(
            db.desc(StudentResults.total_score)
        ).all()
        # convert query to list of scores
        subject_total_scores = [x[0] for x in subject_total_scores_query]
        student_score_index = subject_total_scores.index(student_total_score)
        pos_engine = inflect.engine()
        return pos_engine.ordinal(student_score_index + 1)


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))
