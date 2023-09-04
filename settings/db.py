import datetime
from weakref import WeakValueDictionary
from sqlalchemy import inspect
from sqlalchemy.orm import aliased
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class BaseModel:
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """ Define a base way to print models
            Columns inside `print_filter` are excluded """
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        })

    to_json_filter = ()

    @property
    def json(self):
        """ Define a base way to jsonify models
            Columns inside `to_json_filter` are excluded """
        return {
            column: value if not isinstance(value, datetime.date) else value.isoformat()
            for column, value in self._to_dict().items()
            if column not in self.to_json_filter
        }

    def _to_dict(self):
        """ This would more or less be the same as a `to_json`
            But putting it in a "private" function
            Allows to_json to be overriden without impacting __repr__
            Or the other way around
            And to add filter lists """
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_objects_by_id(self, id=None):
        return self.query.filter_by(id=id).first()
