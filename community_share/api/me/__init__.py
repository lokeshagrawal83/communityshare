from . import get_me


def register_routes(app):
    app.route(
        '/rest/me/',
        methods=['GET'],
        endpoint='me',
        strict_slashes=False,
    )(get_me.endpoint)
