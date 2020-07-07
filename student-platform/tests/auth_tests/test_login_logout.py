def test_login_as_admin(test_client, sample_users):
    admin, _ = sample_users
    resp = test_client.post("/auth/login", data=dict(username=admin.username, password="password"),
                            follow_redirects=True)
    assert admin.check_password("password")
    assert b'Welcome %b' % admin.username.encode('utf8') in resp.data
    assert resp.status_code == 200
    # logout
    resp2 = test_client.get(
        "/auth/logout",
        follow_redirects=True
    )
    assert resp2.status_code == 200


def test_login_as_user(test_client, sample_users):
    _, user = sample_users
    resp = test_client.post(
        "/auth/login",
        data=dict(
            username=user.username,
            password="password"
        ),
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert b'Welcome %b' % user.username.encode('utf8') in resp.data
    resp2 = test_client.get(
        "/auth/logout",
        follow_redirects=True
    )
    assert resp2.status_code == 200
