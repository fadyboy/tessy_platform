from hashlib import md5
from flask import request, url_for
from flask import current_app
from datetime import datetime


def avatar(email, size):
    digest = md5(email.lower().encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


def create_pagination_for_page_view(model_object, view_function):
    page = request.args.get("page", 1, type=int)
    pagination_object = model_object\
        .query.paginate(page, current_app.config["MAX_USERS_PER_PAGE"], False)
    next_url = url_for(view_function, page=pagination_object.next_num) \
        if pagination_object.has_next else None
    prev_url = url_for(view_function, page=pagination_object.prev_num) \
        if pagination_object.has_prev else None
    return pagination_object, next_url, prev_url


def get_student_results(student_id, term, session_id, classroom_id,
                        result_model, subject_model):
    """
    Helper method to get the results for a given student
    """
    student_results = result_model.query.filter_by(
        student_id=student_id, term=term,
        sessions_id=session_id
    ).order_by(
        result_model.subject_id
    ).all()

    # student = Student.query.get(student_id)
    # classroom_id = student.classroom_id
    records = []
    for record in student_results:
        record_details = {}
        subject = subject_model.query.get(record.subject_id)
        record_details["subject_name"] = subject.name
        record_details["ca_score"] = record.ca_score
        record_details["exam_score"] = record.exam_score
        record_details["total"] = record.total_score
        record_details["grade"] = record.grade
        record_details["remark"] = record.grade_remark
        avg_score = result_model.calculate_subject_average_score_in_class(
            record.subject_id, classroom_id, term, session_id
        )
        record_details["average_score"] = avg_score
        score_pos = result_model.calculate_score_position_in_subject(
            record.subject_id, classroom_id, term, session_id,
            record.total_score
        )
        record_details["score_position"] = score_pos
        records.append(record_details)
    return records


def create_datetime_from_str(date_string):
    """ Helper method to convert a date string to a python date object """
    return datetime.strptime(date_string, "%Y-%m-%d")
