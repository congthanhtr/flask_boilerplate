from flask import Blueprint, request, jsonify
from .model import Role
from flask.views import MethodView
from .role_service import RoleService
from .role_repository import RoleRepository

role = Blueprint('role', __name__)


class RoleView(MethodView):

    def __init__(self, _service: RoleService):
        self.service = _service

    def get(self):
        roles = self.service.get_all_objects()
        return jsonify([role.role_name for role in roles])

    def post(self):  # create a new role
        body = request.get_json(force=True)
        role_name = body.get('role_name')

        existed_role = self.service.get_object_by_role_name(role_name)
        if not existed_role:
            new_role = Role(role_name=role_name)
            self.service.create_object(new_role)

        return jsonify(msg=f'Role {role_name} created')


role_service = RoleService(RoleRepository())

role.add_url_rule('', view_func=RoleView.as_view('create', role_service))
