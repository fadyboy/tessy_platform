from studentapp import create_app, db
from studentapp.models import (User, Staff, Student, Classroom, Role, Subject,
                               Sessions, StudentResults)
from flask.cli import FlaskGroup

app = create_app()
cli = FlaskGroup(create_app=create_app)


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


@cli.command("create_admin_user")
def create_admin_user():
    role1 = Role(name="Admin")
    role2 = Role(name="User")
    db.session.add_all([role1, role2])
    db.session.commit()

    admin = User(username="admin", email="admin@example.com", role=role1)
    admin.set_password_hash("secret_password")
    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":
    cli()
