from studentapp.models import StudentResults


def test_add_student_scores_to_db(sample_students, test_db, sample_session, sample_subjects):
    s1 = sample_students[0]
    s1_scores = StudentResults(
        student_id=s1.id,
        classroom_id=s1.classroom_id,
        subject_id=sample_subjects[0].id,
        term="First",
        sessions_id=sample_session.id,
        ca_score=37,
        exam_score=40
    )
    s1_scores.total_score = s1_scores.set_total_score(37, 40)
    grade, remark = s1_scores.set_grade_and_remark(s1_scores.total_score)
    s1_scores.grade = grade
    s1_scores.grade_remark = remark
    test_db.session.add(s1_scores)
    test_db.session.commit()
    s1_saved_result = StudentResults.query.filter_by(student_id=s1.id).first()
    assert s1_saved_result.ca_score == 37
    assert s1_saved_result.exam_score == 40


def test_submit_student_score_using_route(test_client, sample_students, sample_session, sample_subjects):
    s1 = sample_students[0]
    resp = test_client.post(
        "/submit_student_scores",
        data=dict(
            student_id=s1,
            classroom_id=s1.classroom_id,
            subject_id=sample_subjects[0].id,
            term="First",
            sessions_id=sample_session.id,
            ca_score=37,
            exam_score=40
        ),
        follow_redirects=True
    )
    assert resp.status_code == 200  #TODO:Fix as this works with invalid values


