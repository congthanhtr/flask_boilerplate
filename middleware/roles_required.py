from functools import wraps
from flask import abort, current_app, g


def roles_required(*role_names):
    def wrapper(view_function):
        @wraps(view_function)
        def decorator(*args, **kwargs):
            current_user = g.current_user
            authenticated = current_user.is_authenticated
            if not authenticated:
                abort(401)

            # User must have the required roles
            if not current_user.has_roles(*role_names):
                abort(404)

            return view_function(*args, **kwargs)

        return decorator

    return wrapper
