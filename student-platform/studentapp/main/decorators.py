from functools import wraps
from flask import session, redirect, url_for, flash


def route_level_access(user_role):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if session["user_role"] not in user_role:
                flash(f"You do not have permission to the {func.__name__} page")
                return redirect(url_for("main.index"))
            return func(*args, **kwargs)

        return decorated_view

    return decorator
