import pdfkit
import csv
from io import StringIO
from flask import (render_template, redirect, request, flash,
                   url_for, make_response, current_app, g)

from studentapp import db
from studentapp.main.forms import (
    AddUserForm, EditUserForm, AddStaffForm, EditStaffForm,
    AddStudentForm, EditStudentForm, AddSubjectForm, EditSubjectForm,
    AddClassroomForm, EditClassroomForm, EnterStudentScoresForm,
    SubmitStudentScoresForm, AddSessionForm, SetActiveSessionForm,
    UploadImageForm, BulkUploadForm, SearchForm
)
from studentapp.models import (
    User, Staff, Student, Subject, Classroom, Sessions,
    StudentResults
)
from distutils.util import strtobool
from studentapp.utils import (create_pagination_for_page_view,
                              get_student_results, create_datetime_from_str,
                              search_model)
from flask_uploads import configure_uploads, UploadSet, IMAGES, DATA
from studentapp.main import bp
from flask_login import login_required, current_user
from .decorators import route_level_access
from sqlalchemy import exc

# settings for uploading images
images = UploadSet("images", IMAGES)
data = UploadSet("data", DATA)
configure_uploads(current_app, (images, data))


@bp.before_app_request
def before_request():
    # set the SearchForm as part of flask global to access throught request
    # add just before request
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    total_male_students = Student.get_total_students_by_gender("Male")
    total_female_students = Student.get_total_students_by_gender("Female")
    total_students = total_male_students + total_female_students
    student_totals = dict(male=total_male_students,
                          female=total_female_students,
                          total=total_students)
    list_of_classrooms = Classroom.list_classrooms()
    gender_dist_by_class = []
    for classroom in list_of_classrooms:
        gender_dist_by_class_obj = {}
        gender_dist_by_class_obj["class_id"] = classroom.id
        gender_dist_by_class_obj["male"] = Student. \
            get_gender_total_in_class(
            "Male",
            classroom.id
        )
        gender_dist_by_class_obj["female"] = Student. \
            get_gender_total_in_class(
            "Female",
            classroom.id
        )
        gender_dist_by_class.append(gender_dist_by_class_obj)

    return render_template("index.html", title="Home",
                           student_totals=student_totals,
                           gender_dist_list=gender_dist_by_class,
                           classroom_list=list_of_classrooms)


@bp.route("/add_user", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password_hash(form.password.data)
        user.role = form.roles.data
        db.session.add(user)
        db.session.commit()
        flash(f"{user.username} user added")
        # re-index table for searches
        User.reindex()
        return redirect(url_for("main.add_user"))
    return render_template("add_user.html", title="Add User", form=form)


@bp.route("/add_staff", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def add_staff():
    form = AddStaffForm()
    if form.validate_on_submit():
        staff_user = Staff(
            serial_number=form.serial_number.data,
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
        flash(f"{staff_user.firstname} {staff_user.surname} added as a member \
            of staff")
        # re-index table for searches
        Staff.reindex()
        return redirect(url_for("main.add_staff"))
    return render_template("add_staff.html", title="Add Staff", form=form)


@bp.route("/add_student", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
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
        # re-index table for searches
        Student.reindex()
        return redirect(url_for("main.add_student"))
    return render_template("add_student.html", title="Add Student",
                           form=form)


@bp.route("/add_classroom", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
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
        return redirect(url_for("main.add_classroom"))
    return render_template("add_classroom.html", title="Add Classroom",
                           form=form)


@bp.route("/add_subject", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
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
        return redirect(url_for("main.add_subject"))
    return render_template("add_subject.html", title="Add Subject",
                           form=form)


@bp.route("/add_session", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def add_session():
    form = AddSessionForm()
    if form.validate_on_submit():
        school_session = Sessions(
            session=form.session.data,
            current_session=False
        )
        db.session.add(school_session)
        db.session.commit()
        flash(f"{school_session.session} added")
        return redirect(url_for("main.add_session"))
    return render_template("add_session.html", title="Add School Session",
                           form=form)


@bp.route("/list_users")
@login_required
def list_users():
    users, next_url, prev_url = \
        create_pagination_for_page_view(User, "main.list_users")
    return render_template("list_users.html", title="All Users",
                           users=users.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route("/list_staff")
@login_required
def list_staff():
    staff, next_url, prev_url = \
        create_pagination_for_page_view(Staff, "main.list_staff")
    return render_template("list_staff.html", title="All Staff",
                           staff=staff.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route("/list_students")
@login_required
def list_students():
    students, next_url, prev_url = \
        create_pagination_for_page_view(Student, "main.list_students")
    return render_template("list_students.html", title="All Students",
                           students=students.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route("/list_subjects")
@login_required
def list_subjects():
    subjects, next_url, prev_url = \
        create_pagination_for_page_view(Subject, "main.list_subjects")
    return render_template("list_subjects.html", title="List Subjects",
                           subjects=subjects.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route("/list_classrooms")
@login_required
def list_classrooms():
    classrooms, next_url, prev_url = \
        create_pagination_for_page_view(Classroom, "main.list_classrooms")
    return render_template("list_classrooms.html",
                           title="List Classrooms",
                           classrooms=classrooms.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route("/user/<id>")
@login_required
def user(id):
    form = UploadImageForm()
    user = User.query.get_or_404(id, description="User not found")
    return render_template("user.html", title="User Profile",
                           user=user, form=form)


@bp.route("/staff/<id>")
@login_required
def staff(id):
    form = UploadImageForm()
    staff = Staff.query.get_or_404(id, description="Staff not found")
    return render_template("staff.html", title="Staff Profile",
                           staff=staff, form=form)


@bp.route("/student/<id>")
@login_required
def student(id):
    form = UploadImageForm()
    student = Student.query.get_or_404(id, description="Student not found")
    return render_template("student.html", title="Student Profile",
                           student=student, form=form)


@bp.route("/edit_user/<id>", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def edit_user(id):
    user = User.query.get(id)
    form = EditUserForm(
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        roles=user.role
    )
    if form.validate_on_submit():
        user.set_password_hash(form.password.data)
        user.is_active = bool(strtobool(form.is_active.data))
        user.role = form.roles.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("main.user", id=id))

    return render_template("edit_user.html",
                           title="Edit User Profile",
                           form=form, user=user)


@bp.route("/edit_staff/<id>", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def edit_staff(id):
    staff = Staff.query.get(id)
    form = EditStaffForm(
        serial_number=staff.serial_number,
        firstname=staff.firstname,
        middlename=staff.middlename,
        surname=staff.surname,
        contact_number=staff.contact_number,
        email=staff.email,
        address=staff.address
    )
    if form.validate_on_submit():
        staff.firstname = form.firstname.data
        staff.middlename = form.middlename.data
        staff.surname = form.surname.data
        staff.contact_number = form.contact_number.data
        staff.email = form.email.data
        staff.address = form.address.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("main.staff", id=id))
    return render_template("edit_staff.html",
                           title="Edit Staff Profile",
                           form=form, staff=staff)


@bp.route("/edit_student/<id>", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def edit_student(id):
    student = Student.query.get(id)
    # get classroom object to pre-populate classroom selection
    classroom = Classroom.query.get(student.classroom_id)
    form = EditStudentForm(
        serial_number=student.serial_number,
        firstname=student.firstname,
        middlename=student.middlename,
        surname=student.surname,
        contact_number=student.contact_number,
        email=student.email,
        address=student.address,
        classrooms=classroom
    )

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
        return redirect(url_for("main.student", id=id))
    return render_template("edit_student.html", title="Edit Student Profile",
                           form=form, student=student)


@bp.route("/edit_subject/<id>", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def edit_subject(id):
    subject = Subject.query.get(id)
    form = EditSubjectForm(
        name=subject.name,
        code=subject.code
    )
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.code = form.code.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("main.list_subjects"))
    return render_template("edit_subject.html", title="Edit Subject",
                           subject=subject, form=form)


@bp.route("/edit_classroom/<id>", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def edit_classroom(id):
    classroom = Classroom.query.get(id)
    form = EditClassroomForm(
        classroom_name=classroom.classroom_name,
        classroom_symbol=classroom.classroom_symbol
    )
    if form.validate_on_submit():
        classroom.classroom_name = form.classroom_name.data
        classroom.classroom_symbol = form.classroom_symbol.data
        db.session.commit()
        flash("Changes have been submitted")
        return redirect(url_for("main.list_classrooms"))
    return render_template("edit_classroom.html", title="Edit Classrooms",
                           form=form, classroom=classroom)


@bp.route("/select_score_options", methods=["GET", "POST"])
@login_required
def select_score_options():
    form = EnterStudentScoresForm()

    if form.validate_on_submit():
        subject = form.subject.data
        classroom = form.classroom.data
        sessions = form.sessions.data
        term = form.term.data
        return redirect(
            url_for("main.submit_student_scores", subject=subject,
                    classroom=classroom, sessions=sessions, term=term))
    return render_template("select_score_options.html",
                           title="Select Score Options", form=form)


@bp.route("/submit_student_scores", methods=["GET", "POST"])
@login_required
def submit_student_scores():
    subject_name = request.args.get("subject").split(":")[1].strip()
    subject = Subject.query.filter_by(name=subject_name).first()
    classroom_sym = request.args.get("classroom").split(":")[1].strip()
    classroom = Classroom.query.filter_by(
        classroom_symbol=classroom_sym
    ).first()
    term = request.args.get("term")
    students_query = Student.query.filter_by(classroom_id=classroom.id).all()
    students_list = []
    session_name = request.args.get("sessions").split(":")[1].strip()
    sessions = Sessions.query.filter_by(session=session_name).first()
    for student in students_query:
        students_list.append(student)

    form = SubmitStudentScoresForm()
    if form.validate_on_submit():
        # check if record exists already
        record_exists = \
            StudentResults.query.filter_by(student_id=form.student_id.data,
                                           classroom_id=form.classroom_id.data,
                                           subject_id=form.subject_id.data,
                                           term=form.term.data,
                                           sessions_id=form.sessions_id.data
                                           ).first()
        if record_exists is not None:
            flash("Record already exists for student in subject for \
                  term and session")
        else:
            ca_score = int(form.ca_score.data)
            exam_score = int(form.exam_score.data)
            result = StudentResults(
                student_id=form.student_id.data,
                classroom_id=form.classroom_id.data,
                subject_id=form.subject_id.data,
                term=form.term.data,
                sessions_id=form.sessions_id.data,
                ca_score=ca_score,
                exam_score=exam_score
            )
            total_score = result.set_total_score(ca_score, exam_score)
            result.total_score = total_score
            grade, remark = result.set_grade_and_remark(total_score)
            result.grade = grade
            result.grade_remark = remark
            db.session.add(result)
            db.session.commit()
            added_student = Student.query.get(form.student_id.data)
            flash(f"Result added for {added_student}")
        return redirect(
            url_for("main.submit_student_scores", subject=subject,
                    classroom=classroom, term=term, sessions=sessions))

    return render_template("submit_student_scores.html", form=form,
                           subject=subject, term=term, classroom=classroom,
                           sessions=sessions, students=students_list)


@bp.route("/view_student_result")
@login_required
def view_student_result():
    term = request.args.get("term")
    student_id = request.args.get("id")
    active_session = Sessions.query.filter_by(current_session=True).first()
    student = Student.query.get(student_id)
    classroom_id = student.classroom_id
    records = get_student_results(
        student_id, term, active_session.id, classroom_id,
        StudentResults, Subject
    )

    return render_template("view_student_result.html",
                           title="View Student Result",
                           records=records,
                           student=student,
                           term=term,
                           active_session=active_session)


@bp.route("/set_active_session", methods=["GET", "POST"])
@login_required
@route_level_access(["Admin"])
def set_active_session():
    form = SetActiveSessionForm()
    if form.validate_on_submit():
        selected_session = form.session.data
        selected_session.set_as_current_session(selected_session.id)
        selected_session.set_as_current_session(selected_session.id)
        db.session.add(selected_session)
        db.session.commit()
        flash(f"{selected_session.session} set as current session")

    return render_template("set_active_session.html",
                           title="Set Active Session", form=form)


@bp.route("/upload_image", methods=["GET", "POST"])
@login_required
def upload_image():
    # add variables for the url_function, person object, and object id
    url_func = None
    person_obj = None
    obj_id = None
    if request.method == "POST":
        obj_id = request.args.get("id")
        obj_type = request.args.get("obj_type")
        if obj_type == "Student":
            person_obj = Student.query.get(obj_id)
            url_func = "main.student"
        elif obj_type == "Staff":
            person_obj = Staff.query.get(obj_id)
            url_func = "main.staff"
        elif obj_type == "User":
            person_obj = User.query.get(obj_id)
            url_func = "main.user"
        image_file = request.files["image_file"]
        if image_file.filename == "":
            flash("No image file selected")
            return redirect(url_for(url_func, id=obj_id))
        if image_file.filename != "":
            image_file_name = images.save(image_file)
            person_obj.image_file_name = image_file_name
            db.session.commit()
            flash("Image saved!")
    return redirect(url_for(url_func, id=obj_id))


@bp.route("/download_report_pdf")
def download_report_pdf():
    term = request.args.get("term")
    student = Student.query.get(request.args.get("student_id"))
    active_session = request.args.get("active_session")
    records = get_student_results(
        student.id, term, active_session,
        student.classroom_id, StudentResults,
        Subject
    )
    student_report_template = render_template("student_report.html",
                                              student=student, term=term,
                                              active_session=active_session,
                                              records=records)

    css_file = "studentapp/static/css/bulma.min.css"
    student_pdf_report = pdfkit.from_string(student_report_template, False,
                                            css=css_file)
    resp = make_response(student_pdf_report)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f"attachment;filename=\
        {student.firstname}_{student.surname}_report.pdf"

    return resp


@bp.route("/bulk_upload", methods=["GET", "POST"])
@login_required
def bulk_upload():
    """
    - upload file
    """
    form = BulkUploadForm()
    if form.validate_on_submit():
        bulk_upload_file = request.files["bulk_upload_file"]
        object_type = form.upload_object.data
        # catch error if file is not csv file
        try:
            data_stream = StringIO(bulk_upload_file.stream.read().decode("UTF-8"), newline=None)
        except UnicodeDecodeError:
            flash("Unable to read csv file, please ensure you have the right file type")
            return redirect(url_for("main.bulk_upload"))  # return user to bulk upload form
        bulk_data = csv.reader(data_stream)
        next(bulk_data)  # skip header row
        bulk_upload_objects = []
        serial_nums = {}
        if object_type == "Student":
            for row in bulk_data:
                # check if serial number in dict
                if serial_nums.get(row[0]) is None:
                    serial_nums[row[0]] = 1
                else:
                    flash(f"A record with this serial number - {row[0]} already exists, record will be skipped")
                    continue
                try:
                    record = Student(
                        serial_number=row[0],
                        firstname=row[1],
                        middlename=row[2],
                        surname=row[3],
                        gender=row[4],
                        birthday=create_datetime_from_str(row[5]),
                        contact_number=row[6],
                        email=row[7],
                        parent_guardian_name=row[8],
                        address=row[9],
                        classroom_id=Classroom.get_classroom_id_from_symbol(row[10])
                    )
                    bulk_upload_objects.append(record)
                except (TypeError, ValueError) as e:
                    flash(f"Error: Incorrect field name or field type in record - {row}")
                    print(f"Error - {e}")
                    continue
            # add exception handler for if duplicate record already exists in db
            try:
                db.session.bulk_save_objects(bulk_upload_objects)
                db.session.commit()
            except exc.IntegrityError:
                flash("Duplicate record(s) found in list, unable to carry out batch update")
            return redirect(url_for("main.bulk_upload"))
        elif object_type == "Staff":
            for row in bulk_data:
                # check if serial number in dict
                if serial_nums.get(row[0]) is None:
                    serial_nums[row[0]] = 1
                else:
                    flash(f"A record with this serial number - {row[0]} already exists, record will be skipped")
                    continue
                try:
                    record = Staff(
                        serial_number=row[0],
                        firstname=row[1],
                        middlename=row[2],
                        surname=row[3],
                        gender=row[4],
                        birthday=create_datetime_from_str(row[5]),
                        contact_number=row[6],
                        email=row[7],
                        address=row[8]
                    )
                    bulk_upload_objects.append(record)
                except (TypeError, ValueError) as e:
                    flash(f"Error: Incorrect field name or field type in record - {row}")
                    print(f"Error - {e}")
                    continue
            # add exception handler for if duplicate record already exists in db
            try:
                db.session.bulk_save_objects(bulk_upload_objects)
                db.session.commit()
            except exc.IntegrityError:
                flash("Duplicate record(s) exists in list, unable to carry out batch update")
            return redirect(url_for("main.bulk_upload"))

    return render_template("bulk_upload.html", title="Bulk Uploads", form=form)


@bp.route("/search")
@login_required
def search():
    page = request.args.get("page", 1, type=int)
    query = g.search_form.q.data
    search_obj = g.search_form.search_obj.data
    if search_obj == "Students":
        results, next_url, prev_url = search_model(Student, query, page)
    elif search_obj == "Staff":
        results, next_url, prev_url = search_model(Staff, query, page)
    elif search_obj == "User":
        results, next_url, prev_url = search_model(User, query, page)

    return render_template("search.html", title="Search Results", results=results,
                           next_url=next_url, prev_url=prev_url)
