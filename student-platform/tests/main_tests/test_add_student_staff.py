from studentapp.models import Student, Staff
from datetime import datetime


def test_create_student(test_db, sample_classroom):
    # create classroom to associate class with student
    classroom_1 = sample_classroom
    student1 = Student(
        serial_number="test/123",
        firstname="Adam",
        middlename="Evan",
        surname="Smith",
        gender="Male",
        birthday=datetime.strptime("2007-02-28", "%Y-%m-%d"),
        contact_number="08033383748",
        email="as@example.com",
        parent_guardian_name="Walter Smith",
        address="123 Nondescript Street, Portharcourt",
        classroom_id=classroom_1.id
    )
    test_db.session.add(student1)
    test_db.session.commit()
    saved_student = Student.query.get(1)
    assert saved_student.serial_number == student1.serial_number
    assert saved_student.firstname == student1.firstname
    assert saved_student.surname == student1.surname


def test_add_staff(test_db):
    staff = Staff(
        serial_number="tessy/staff/123",
        firstname="Johnson",
        surname="Igwe",
        gender="Male",
        birthday=datetime.strptime("1986-05-12", "%Y-%m-%d"),
        contact_number="08069389933",
        email="ji@example.com",
        address="123 Hogan Bassey, Portharcourt"
    )
    test_db.session.add(staff)
    test_db.session.commit()
    saved_staff = Staff.query.get(1)
    assert saved_staff.serial_number == staff.serial_number
    assert saved_staff.firstname == staff.firstname
    assert saved_staff.surname == staff.surname