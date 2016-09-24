from . import analytics
from . import users


def register_routes(app):
    analytics.register_routes(app)
    users.register_routes(app)
