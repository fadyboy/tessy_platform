import pytest
from datetime import datetime
from studentapp import create_app, db
from studentapp.models import User, Role, Classroom, Subject, Sessions, Student
from config import TestConfig


@pytest.fixture(scope="module")
def test_client():
    app = create_app(TestConfig)
    testing_client = app.test_client()  # use the Wierkzurg flask test client
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope="module")
def test_db(test_client):
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def sample_users(test_db):
    admin_role = Role(name="Admin")
    user_role = Role(name="User")
    admin_user = User(username="admin", email="admin@example.com", role=admin_role, is_active=True)
    user = User(username="user1", email="user1@example.com", role=user_role, is_active=True)
    admin_user.set_password_hash("password")
    user.set_password_hash("password")
    db = test_db
    db.session.add(admin_user)
    db.session.add(user)
    db.session.commit()
    yield admin_user, user


@pytest.fixture(scope="module")
def sample_classroom(test_db):
    classroom_1 = Classroom(
        classroom_name="Junior Secondary 1A",
        classroom_symbol="JS1A"
    )
    test_db.session.add(classroom_1)
    test_db.session.commit()
    saved_classroom = Classroom.query.get(1)
    assert saved_classroom.classroom_name == classroom_1.classroom_name
    yield classroom_1


@pytest.fixture(scope="module")
def sample_subjects(test_db):
    sub_1 = Subject(
        name="Junior Maths 1",
        code="JMth1"
    )
    sub_2 = Subject(
        name="Junior English 1",
        code="JEng1"
    )
    sub_3 = Subject(
        name="Junior Science 1",
        code="JSci1"
    )
    test_db.session.add_all([sub_1, sub_2, sub_3])
    test_db.session.commit()

    saved_subjects = Subject.query.all()
    assert saved_subjects[0].name == sub_1.name
    assert saved_subjects[1].name == sub_2.name
    assert saved_subjects[2].name == sub_3.name
    yield saved_subjects


@pytest.fixture(scope="module")
def sample_session(test_db):
    sess_1 = Sessions(
        session="2020/2021",
        current_session=True
    )
    test_db.session.add(sess_1)
    test_db.session.commit()
    saved_session = Sessions.query.get(1)
    assert saved_session.session == sess_1.session
    assert saved_session.current_session
    yield sess_1


@pytest.fixture(scope="module")
def sample_students(test_db, sample_classroom):
    student_1 = Student(
        serial_number="001",
        firstname="John",
        surname="Doe",
        gender="Male",
        birthday=datetime.strptime("2007-02-28", "%Y-%m-%d"),
        contact_number="08033383748",
        email="jd1@example.com",
        parent_guardian_name="Walter Doe",
        address="123 Nondescript Street, Portharcourt",
        classroom_id=sample_classroom.id
    )
    student_2 = Student(
        serial_number="002",
        firstname="Jane",
        surname="Doe",
        gender="Female",
        birthday=datetime.strptime("2008-09-19", "%Y-%m-%d"),
        contact_number="08033383747",
        email="jd2@example.com",
        parent_guardian_name="Sam Doz",
        address="321 Nondescript Street, Portharcourt",
        classroom_id=sample_classroom.id
    )
    test_db.session.add_all([student_1, student_2])
    test_db.session.commit()
    yield [student_1, student_2]
