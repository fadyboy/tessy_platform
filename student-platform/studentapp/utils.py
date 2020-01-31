from hashlib import md5


def avatar(email, size, default_pic=None):
    digest = md5(email.lower().encode("utf-8")).hexdigest()
    if not default_pic:
        default_pic = "identicon"
    return f"https://www.gravatar.com/avatar/{digest}?d={default_pic}&s={size}"