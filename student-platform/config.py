import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{os.path.join(basedir, 'studentapp.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # configure how many users, students, staff displayed on page
    MAX_USERS_PER_PAGE = 5

    # Mail server settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["aofadero@gmail.com"]  # TODO: Add email address

    # profile pictures upload folder
    UPLOADED_IMAGES_DEST = os.path.join(
        basedir, "studentapp/static/images/profile_pics"
        )
