import datetime
from ...settings.db import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from ...settings.config import Config
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(db.Model, BaseModel):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    role_id = db.Column('role_id', db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='role')
    full_name = db.Column(db.String(150), default=1)

    def __init__(self, email=None, password=None):
        if email:
            self.email = email.lower()

        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_token(self):
        payload = {
            'email': self.email,
            'id': str(self.id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        return jwt.encode(payload=payload, key=Config.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
            return payload
        except jwt.exceptions.ExpiredSignatureError:
            return 'Expired signature'
        except jwt.exceptions.InvalidTokenError as invalid_token:
            return str(invalid_token)
        except Exception as e:
            return str(e)

    def has_roles(self, *requirements):
        user_roles = [role.name for role in self.role]
        for requirement in requirements:
            if requirement not in user_roles:
                return False
        return True


