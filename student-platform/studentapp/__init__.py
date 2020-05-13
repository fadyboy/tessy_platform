import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "auth.login"
mail = Mail(app)

# Register blueprints
from studentapp.errors import bp as errors_bp
from studentapp.auth import bp as auth_bp
from studentapp.main import bp as main_bp

app.register_blueprint(errors_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(main_bp)

if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr=f"no-reply@{app.config['MAIL_SERVER']}",
            toaddrs=app.config["ADMINS"],
            subject="Student Platform Application Failure",
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # application logging
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/studentapp.log", maxBytes=10240, backupCount=10
        )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s in [%(pathname)s:%(lineno)d]"
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("StudentApp startup")

from studentapp import models
