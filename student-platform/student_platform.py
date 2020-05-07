from studentapp import app, db
from studentapp.models import User, Staff, Student, Classroom, Role, Subject,\
    Sessions, StudentResults


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Staff": Staff,
        "Student": Student,
        "Classroom": Classroom,
        "Role": Role,
        "Subject": Subject,
        "Session": Sessions,
        "Results": StudentResults
        }
