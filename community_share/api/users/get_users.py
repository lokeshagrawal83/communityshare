from flask import jsonify, request

from community_share.flask_helpers import api_path, needs_auth
from community_share.models.user import User
from community_share.utils import clamped, int_or


@needs_auth()
def endpoint(requester):
    number = clamped(1, 100, int_or(request.args.get('number'), 10))
    offset = max(0, int_or(request.args.get('offset'), 0))

    search_text = request.args.get('search_text', None)
    created_after = request.args.get('created_after', None)
    created_before = request.args.get('created_before', None)

    users, count = get_users(
        requester,
        search_text=search_text,
        created_after=created_after,
        created_before=created_before,
        number=number,
        offset=offset,
    )

    next_offset = offset if count < number else offset + number

    return jsonify({
        'users': users,
        'meta': {
            'prev_page': api_path('users', {
                'number': number,
                'offset': max(0, offset - number),
            }),
            'next_page': api_path('users', {
                'number': number,
                'offset': next_offset,
            }),
        },
    })


def get_users(
        requesting_user,
        search_text=None,
        created_after=None,
        created_before=None,
        number=10,
        offset=0,
):
    users = User.search(
        search_text,
        created_after,
        created_before,
        number=number,
        offset=offset,
    )
    count = users.count()

    users = [user.serialize(requesting_user) for user in users]
    users = [user for user in users if user is not None]

    return users, count
