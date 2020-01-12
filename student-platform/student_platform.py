from studentapp import app, db
from studentapp.models import Users, Staff, Student, Classroom


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Users": Users, "Staff": Staff, "Student": Student, "Classroom": Classroom}