from http import HTTPStatus

from flask import request

from community_share.flask_helpers import needs_auth, with_store
from community_share.models.analytics import PageView
from community_share.routes.base_routes import make_bad_request_response


@needs_auth()
def endpoint(requester):
    data = request.get_json()

    if data is None:
        return make_bad_request_response('Please provide JSON payload for tracking')

    next_path = data.get('next_path', '')[:255]
    prev_path = data.get('prev_path', '')[:255]

    if record_view(requester.id, next_path, prev_path):
        return '', HTTPStatus.NO_CONTENT

    return make_bad_request_response('Please provide non-empty `next_path` and `prev_path` to track')


@with_store
def record_view(user_id, next_path, prev_path, store=None):
    if not is_valid_path(next_path) or not is_valid_path(prev_path):
        return False

    store.session.add(PageView(user_id, next_path, prev_path))
    store.session.commit()

    return True


def is_valid_path(path):
    if not type(path) == str:
        return False

    if path == "":
        return False

    return True
