from typing import Optional

from flask import request

from community_share import Store, with_store
from community_share.models.secret import lookup_secret
from community_share.models.user import User


def get_requesting_user() -> Optional[User]:
    authorization = request.headers.get('Authorization', None)

    try:
        auth_type, method, value = authorization.split(':')
    except:
        return None

    if 'Basic' != auth_type:
        return None

    if 'api' == method:
        return user_from_api_key(value)

    # Must have an email, password pair
    return user_from_login(method, value)


@with_store
def user_from_api_key(key: str, store: Store=None) -> Optional[User]:
    secret = lookup_secret(key)

    if secret is None:
        return None

    info = secret.get_info()

    if info.get('action') != 'api_key':
        return None

    return store.session.query(User).get(info.get('userId'))


@with_store
def user_from_login(email: str, password: str, store: Store=None) -> Optional[User]:
    user = store.session.query(User)
    user = user.filter_by(email=email, active=True)
    user = user.first()

    if not user.is_password_correct(password):
        return None

    return user
