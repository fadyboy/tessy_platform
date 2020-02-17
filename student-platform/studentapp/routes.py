from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from studentapp import app, db
from studentapp.forms import LoginForm, AddUserForm, AddStaffForm, AddStudentForm, AddClassroomForm, AddSubjectForm, \
    EditUserForm, EditStaffForm, EditStudentForm, EditSubjectForm, EditClassroomForm
from studentapp.models import User, Staff, Student, Classroom, Subject
from flask_login import current_user, login_user, logout_user, login_required
from studentapp.utils import create_pagination_for_page_view
from distutils.util import strtobool


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f"Invalid username or password provided")
            return redirect(url_for("login"))
        # load user
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc == "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form, title="Log In")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html", title="Admin")


@app.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password_hash(form.password.data)
        user.role = form.roles.data
        db.session.add(user)
        db.session.commit()
        flash(f"{user.username} user added")
        return redirect(url_for("add_user")) # redirect used to clear form
    return render_template("add_user.html", title="Add User", form=form)


@app.route("/add_staff", methods=["GET", "POST"])
@login_required
def add_staff():
    form = AddStaffForm()
    if form.validate_on_submit():
        staff_user = Staff(
            serial_number = form.serial_number.data,
            firstname=form.firstname.data,
            middlename=form.middlename.data,
            surname=form.surname.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(staff_user)
        db.session.commit()
        flash(f"{staff_user.firstname} {staff_user.surname} added as a member of staff")
        return redirect(url_for("add_staff"))
    return render_template("add_staff.html", title="Add Staff", form=form)


@app.route("/add_student", methods=["GET", "POST"])
@login_required
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        # get classroom id
        classroom = form.classrooms.data
        student = Student(
            serial_number=form.serial_number.data,
            firstname=form.firstname.data,
            middlename=form.middlename.data,
            surname=form.surname.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            parent_guardian_name=form.parent_guardian_name.data,
            address=form.address.data,
            classroom_id=classroom.id
        )
        db.session.add(student)
        db.session.commit()
        flash(f"Student - {student.firstname} {student.surname} added")
        return redirect(url_for("add_student"))
    return render_template("add_student.html", title="Add Student", form=form)


@app.route("/add_classroom", methods=["GET", "POST"])
@login_required
def add_classroom():
    form = AddClassroomForm()
    if form.validate_on_submit():
        classroom = Classroom(
            classroom_name=form.classroom_name.data,
            classroom_symbol=form.classroom_symbol.data
        )
        db.session.add(classroom)
        db.session.commit()
        flash(f"{classroom.classroom_symbol} classroom added")
        return redirect(url_for("add_classroom"))
    return render_template("add_classroom.html", title="Add Classroom", form=form)


@app.route("/add_subject", methods=["GET", "POST"])
@login_required
def add_subject():
    form = AddSubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            code=form.code.data
        )
        db.session.add(subject)
        db.session.commit()
        flash(f"{subject.name} added as a subject")
        return redirect(url_for("add_subject"))
    return render_template("add_subject.html", title="Add Subject", form=form)


@app.route("/list_users")
@login_required
def list_users():
    users, next_url, prev_url = create_pagination_for_page_view(User, "list_users")
    return render_template("list_users.html", title="All Users", users=users.items, next_url=next_url,
                           prev_url=prev_url)


@app.route("/user/<id>")
@login_required
def user(id):
    user = User.query.get_or_404(id, description="User not found")
    return render_template("user.html", title="User Profile", user=user)


@app.route("/edit_user/<id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    form = EditUserForm()
    user = User.query.get(id)
    if form.validate_on_submit():
        user.set_password_hash(form.password.data)
        user.is_active = bool(strtobool(form.is_active.data))
        user.role = form.roles.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("user", id=id))

    return render_template("edit_user.html", title="Edit User Profile", form=form, user=user)


@app.route("/list_staff")
@login_required
def list_staff():
    staff, next_url, prev_url = create_pagination_for_page_view(Staff, "list_staff")
    return render_template("list_staff.html", title="All Staff", staff=staff.items, next_url=next_url,
                           prev_url=prev_url)


@app.route("/list_all_students")
@login_required
def list_students():
    students, next_url, prev_url = create_pagination_for_page_view(Student, "list_students")
    return render_template("list_students.html", title="All Students", students=students.items, next_url=next_url,
                           prev_url=prev_url)


@app.route("/staff/<id>")
@login_required
def staff(id):
    staff = Staff.query.get_or_404(id, description="Staff not found")
    return render_template("staff.html", title="Staff Profile", staff=staff)


@app.route("/student/<id>")
@login_required
def student(id):
    student = Student.query.get_or_404(id, description="Student not found")
    return render_template("student.html", title="Student Profile", student=student)


@app.route("/edit_staff/<id>", methods=["GET", "POST"])
@login_required
def edit_staff(id):
    form = EditStaffForm()
    staff = Staff.query.get(id)
    if form.validate_on_submit():
        staff.firstname = form.firstname.data
        staff.middlename = form.middlename.data
        staff.surname = form.surname.data
        staff.contact_number = form.contact_number.data
        staff.email = form.email.data
        staff.address = form.address.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("staff", id=id))
    return render_template("edit_staff.html", title="Edit Staff Profile", form=form, staff=staff)


@app.route("/edit_student/<id>", methods=["GET", "POST"])
@login_required
def edit_student(id):
    form = EditStudentForm()
    student = Student.query.get(id)
    if form.validate_on_submit():
        classroom = form.classrooms.data
        student.firstname = form.firstname.data
        student.middlename = form.middlename.data
        student.surname = form.surname.data
        student.contact_number = form.contact_number.data
        student.email = form.email.data
        student.address = form.address.data
        student.classroom_id = classroom.id
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("student", id=id))
    return render_template("edit_student.html", title="Edit Student Profile", form=form, student=student)


@app.route("/list_subjects")
@login_required
def list_subjects():
    subjects = Subject.query.all()
    return render_template("list_subjects.html", title="List Subjects", subjects=subjects)


@app.route("/edit_subject/<id>", methods=["GET", "POST"])
@login_required
def edit_subject(id):
    subject = Subject.query.get(id)
    form = EditSubjectForm()
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.code = form.code.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("list_subjects"))
    return render_template("edit_subject.html", title="Edit Subject", subject=subject, form=form)


@app.route("/list_classrooms")
@login_required
def list_classrooms():
    classrooms = Classroom.query.all()
    return render_template("list_classrooms.html", title="List Classrooms", classrooms=classrooms)


@app.route("/edit_classroom/<id>", methods=["GET", "POST"])
@login_required
def edit_classroom(id):
    classroom = Classroom.query.get(id)
    form = EditClassroomForm()
    if form.validate_on_submit():
        classroom.classroom_name = form.classroom_name.data
        classroom.classroom_symbol = form.classroom_symbol.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("list_classrooms"))
    return render_template("edit_classroom.html", title="Edit Classrooms", form=form, classroom=classroom)
