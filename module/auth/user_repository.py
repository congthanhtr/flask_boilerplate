from ...repository import Repository
from .model import User


class UserRepository(Repository):
    _model = User
