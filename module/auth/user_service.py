from .user_repository import UserRepository
from ...service import Service


class UserService(Service):

    _repository: UserRepository

    def get_object_by_email(self, email):
        return self._repository._model.query.filter_by(email=email).first()

