from .repository import Repository


class Service:
    _repository: Repository

    def __init__(self, repository=None):
        self._repository = repository

    def get_object_by_id(self, object_id):
        return self._repository.get_object_by_id(object_id)

    def get_all_objects(self):
        return self._repository.get_all_objects()

    def create_object(self, obj):
        return self._repository.create_object(obj)
