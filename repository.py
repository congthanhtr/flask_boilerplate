from .settings.db import db


class Repository:
    _model: db.Model

    def get_object_by_id(self, id):
        return self._model.query.filter_by(id=id).first()

    def get_all_objects(self):
        return self._model.query.all()

    @staticmethod
    def create_object(obj: db.Model):
        db.session.add(obj)
        db.session.commit()
