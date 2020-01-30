import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(basedir, 'studentapp.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # configure how many users, students, staff displayed on page
    MAX_USERS_PER_PAGE = 3
