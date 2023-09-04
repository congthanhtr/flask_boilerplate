from ...settings.db import db, BaseModel


class Role(db.Model, BaseModel):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255))
    user = db.relationship('User', backref='user', uselist=False)

    def __init__(self, role_name=None):
        self.role_name = role_name
