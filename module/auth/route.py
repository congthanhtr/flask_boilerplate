from flask import Blueprint, request, g
from flask.views import MethodView

from ...middleware.login_required import login_required
from .model import User
from .user_service import UserService
from .user_repository import UserRepository
from ...utils.send_mail import send_mail

auth = Blueprint('auth', __name__)


class LoginView(MethodView):
    def __init__(self, _user_service: UserService) -> None:
        self.service: UserService = _user_service

    def post(self):
        access_token = 'no_token'
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')
        users_with_email: User = self.service.get_object_by_email(email)
        if users_with_email:
            is_legit = users_with_email.check_password(password)
            if is_legit:
                access_token = users_with_email.generate_token()
                g.current_user = users_with_email

        return {'access_token': access_token}


class RegisterView(MethodView):
    def __init__(self, _user_service: UserService) -> None:
        self.service: UserService = _user_service

    def post(self):
        try:
            body = request.get_json(force=True)
            email = body.get('email')
            password = body.get('password')

            # try new one
            user = self.service.get_object_by_email(email)
            if not user:
                new_user = User(email=email)
                new_user.set_password(password)
                user_service.create_object(new_user)

        except Exception as e:
            msg = str(e)
            pass

        return {'msg': 'User successfully created'}


user_service = UserService(UserRepository())

auth.add_url_rule('/login', view_func=LoginView.as_view('login_', user_service))
auth.add_url_rule('/register', view_func=RegisterView.as_view('register', user_service))
