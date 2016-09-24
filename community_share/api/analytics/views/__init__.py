from . import record_view


def register_routes(app):
    app.route(
        '/rest/analytics/views',
        endpoint='anayticsPageViews',
        methods=['POST'],
        strict_slashes=False,
    )(record_view.endpoint)
