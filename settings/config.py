from dotenv import load_dotenv
import os

DEV = True

if DEV:
    load_dotenv('env/dev.env')
else:
    load_dotenv('env/prod.env')


class Config:
    FLASK_APP = 'app.py'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             'postgresql://<user>:<password>@<host>:<port>/<DBName>')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_super_secret')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = bool(os.environ.get('MAIL_USE_SSL', True))
    MAIL_USE_TLS = bool(os.environ.get('MAIL_USE_TLS', False))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    DEBUG = bool(os.environ.get('DEBUG', False))
