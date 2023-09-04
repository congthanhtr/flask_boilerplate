from flask import Flask
from .settings.db import db
from .utils.send_mail import mail
from .settings.config import Config
from flask_migrate import Migrate

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    # existing code omitted

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from .module.auth.route import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .module.role.route import role
    app.register_blueprint(role, url_prefix='/role')

    return app
