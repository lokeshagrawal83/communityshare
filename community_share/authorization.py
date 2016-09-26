import logging

from flask import request

from community_share.flask_helpers import with_store
from community_share.models.secret import lookup_secret
from community_share.models.user import User

logger = logging.getLogger(__name__)


class NotAuthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


def get_requesting_user():
    authorization = request.headers.get('Authorization', None)

    if authorization is None:
        return None

    try:
        auth_type, method, value = authorization.split(':')
    except ValueError:
        return None

    if 'Basic' != auth_type:
        return None

    if 'api' == method:
        return user_from_api_key(value)

    # Must have an email, password pair
    return user_from_login(method, value)


@with_store
def user_from_api_key(key, store=None):
    secret = lookup_secret(key)

    if secret is None:
        return None

    info = secret.get_info()

    if info.get('action') != 'api_key':
        return None

    return store.session.query(User).get(info.get('userId'))


@with_store
def user_from_login(email: str, password: str, store=None):
    user = store.session.query(User)
    user = user.filter_by(email=email, active=True)
    user = user.one_or_none()

    if not user.is_password_correct(password):
        return None

    return user
