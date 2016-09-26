from . import get_user, get_users


def register_routes(app):
    app.route(
        '/rest/users/',
        methods=['GET'],
        endpoint='users',
        strict_slashes=False,
    )(get_users.endpoint)

    app.route(
        '/rest/users/<int:user_id>',
        methods=['GET'],
        endpoint='userById',
        strict_slashes=False,
    )(get_user.endpoint)
