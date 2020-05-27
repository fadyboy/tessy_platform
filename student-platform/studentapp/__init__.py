import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
mail = Mail()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # initialize extensions within the app context
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        login.init_app(app)
        mail.init_app(app)
        moment.init_app(app)

        # Register blueprints
        from studentapp.errors import bp as errors_bp
        from studentapp.auth import bp as auth_bp
        from studentapp.main import bp as main_bp

        app.register_blueprint(errors_bp)
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(main_bp)

        if not app.debug and not app.testing:
            if app.config["MAIL_SERVER"]:
                auth = None
                if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                    auth = (app.config["MAIL_USERNAME"],
                            app.config["MAIL_PASSWORD"])
                secure = None
                if app.config["MAIL_USE_TLS"]:
                    secure = ()
                mail_handler = SMTPHandler(
                    mailhost=(app.config["MAIL_SERVER"],
                              app.config["MAIL_PORT"]),
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
                "%(asctime)s %(levelname)s: %(message)s \
                in [%(pathname)s:%(lineno)d]"
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info("StudentApp startup")
    return app

from studentapp import models
