from functools import wraps

from flask import request

from community_share.authorization import get_requesting_user
from community_share.routes import base_routes


def api_path(path, query_args):
    query = '&'.join(['{}={}'.format(name, query_args[name]) for name in query_args])

    return '{base_url}rest/{path}/{query}'.format(
        base_url=request.url_root,
        path=path,
        query='?{}'.format(query) if query is not '' else ''
    )


def needs_auth(auth_level='user'):
    def needs_auth_decorator(f):
        @wraps(f)
        def auth_check(*args, **kwargs):
            user = get_requesting_user()

            if user is None:
                return base_routes.make_not_authorized_response()

            if 'admin' == auth_level and not user.is_administrator:
                return base_routes.make_not_authorized_response()

            return f(*args, requester=user, **kwargs)

        return auth_check

    return needs_auth_decorator


def needs_admin_auth():
    return needs_auth('admin')
