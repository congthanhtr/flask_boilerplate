from ...repository import Repository
from .model import Role


class RoleRepository(Repository):
    _model = Role

    def get_object_by_role_name(self, role_name):
        return self._model.query.filter_by(role_name=role_name).first()
