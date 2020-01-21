from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from studentapp import app, db
from studentapp.forms import LoginForm, AddUserForm, AddStaffForm, AddStudentForm
from studentapp.models import User, Staff, Student, Classroom
from flask_login import current_user, login_user, logout_user, login_required


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
        staff_user = Staff(firstname=form.firstname.data,
                           middlename=form.middlename.data,
                           surname=form.surname.data,
                           gender=form.gender.data,
                           birthday=form.birthday.data,
                           contact_number=form.contact_number.data,
                           email=form.email.data)
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
            firstname=form.firstname.data,
            middlename=form.middlename.data,
            surname=form.surname.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            parent_guardian_name=form.parent_guardian_name.data,
            classroom_id=classroom.id
        )
        db.session.add(student)
        db.session.commit()
        flash(f"Student - {student.firstname} {student.surname} added")
        return redirect(url_for("add_student"))
    return render_template("add_student.html", title="Add Student", form=form)