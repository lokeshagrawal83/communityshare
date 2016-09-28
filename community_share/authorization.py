from typing import Optional

from flask import request

from community_share import Store, with_store
from community_share.models.secret import lookup_secret
from community_share.models.user import User


def get_requesting_user() -> Optional[User]:
    """Fetch User given Flask request

    :return: logged-in user or None
    """
    authorization = request.headers.get('Authorization', None)

    try:
        auth_type, method, value = authorization.split(':')
    except (AttributeError, ValueError):
        return None

    if auth_type != 'Basic':
        return None

    if method == 'api':
        return user_from_api_key(value)

    # Probably have an email, password pair
    return user_from_login(method, value)


@with_store
def user_from_api_key(key: str, store: Store=None) -> Optional[User]:
    """Fetch User given api key

    :param key: given api key
    :param store: connection to database
    :return: found user or None
    """
    secret = lookup_secret(key)

    if secret is None:
        return None

    info = secret.get_info()

    if info.get('action') != 'api_key':
        return None

    query = store.session.query(User)
    query = query.filter(User.id == info.get('userId'))
    query = query.fitler(User.active == True)

    return query.first()


@with_store
def user_from_login(email: str, password: str, store: Store=None) -> Optional[User]:
    """Fetch User given login credentials

    :param email: given email
    :param password: given password
    :param store: connection to database
    :return: found user or None
    """
    user = store.session.query(User)
    user = user.filter_by(email=email, active=True)
    user = user.first()

    if user is None
        return None

    if not user.is_password_correct(password):
        return None

    return user
