from studentapp.models import User, Role


def test_create_admin_user(test_db):
    admin_role = Role(name="Admin")
    user1 = User(username="fakeUser1", email="fake@example.com", role=admin_role, is_active=True)
    # set password hash
    user1.set_password_hash("password")
    assert user1.check_password("password")
    assert not user1.check_password("cheers")
    db = test_db
    db.session.add(user1)
    db.session.commit()
    saved_user = User.query.get(1)
    assert saved_user.username == "fakeUser1"
    assert saved_user.role == admin_role

