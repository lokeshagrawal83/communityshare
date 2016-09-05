from . import get_users


def register_routes(app):
    app.route('/rest/users/', methods=['GET'])(get_users.endpoint)
