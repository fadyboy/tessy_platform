from studentapp import app, db
from studentapp.models import User, Staff, Student, Classroom, Role


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Staff": Staff, "Student": Student, "Classroom": Classroom, "Role": Role}