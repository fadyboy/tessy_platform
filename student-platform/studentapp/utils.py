from hashlib import md5
from flask import request, url_for
from studentapp import app


def avatar(email, size):
    digest = md5(email.lower().encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


def create_pagination_for_page_view(model_object, view_function):
    page = request.args.get("page", 1, type=int)
    pagination_object = model_object\
        .query.paginate(page, app.config["MAX_USERS_PER_PAGE"], False)
    next_url = url_for(view_function, page=pagination_object.next_num) \
        if pagination_object.has_next else None
    prev_url = url_for(view_function, page=pagination_object.prev_num) \
        if pagination_object.has_prev else None
    return pagination_object, next_url, prev_url
