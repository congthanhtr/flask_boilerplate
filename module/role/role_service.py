from .role_repository import RoleRepository
from ...service import Service


class RoleService(Service):

    _repository: RoleRepository

    def get_object_by_role_name(self, role_name):
        return self._repository.get_object_by_role_name(role_name)

