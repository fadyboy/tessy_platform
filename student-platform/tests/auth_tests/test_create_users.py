import pytest
from studentapp.models import User, Role, Student
from sqlalchemy.exc import IntegrityError


def test_create_admin_user(test_db):
    admin_role = Role(name="Admin")
    user1 = User(username="fakeUser1", email="fake@example.com", role=admin_role, is_active=True)
    user1.set_password_hash("password")
    assert user1.check_password("password")
    assert not user1.check_password("cheers")
    db = test_db
    db.session.add(user1)
    db.session.commit()
    saved_user = User.query.get(1)
    assert saved_user.username == "fakeUser1"
    assert saved_user.role == admin_role


def test_create_normal_user(test_db):
    user_role = Role(name="User")
    user = User(username="User1", email="user1@example.com", role=user_role, is_active=True)
    user.set_password_hash("password")
    assert user.check_password("password")
    db = test_db
    db.session.add(user)
    db.session.commit()
    saved_user = User.query.filter_by(username="User1").first()
    assert saved_user.role == user_role
    assert saved_user.username == "User1"


def test_app_does_not_create_duplicate_users(test_db):
    role = Role(name="User")
    user1 = User(username="User1", email="user1@example.com", role=role, is_active=True)
    user2 = User(username="User1", email="user2@example.com", role=role, is_active=True)
    db = test_db
    db.session.add(user1)
    db.session.add(user2)
    with pytest.raises(IntegrityError):
        db.session.commit()
