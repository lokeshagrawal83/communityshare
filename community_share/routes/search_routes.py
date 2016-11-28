from community_share.models.search import Search, Label
from community_share import search_utils, store
from community_share.app_exceptions import BadRequest, NotFound, Unauthorized, Forbidden
from community_share.routes import base_routes
from community_share.authorization import get_requesting_user
from community_share.utils import is_integer


def register_search_routes(app):

    search_blueprint = base_routes.make_blueprint(Search, 'search')
    app.register_blueprint(search_blueprint)

    @app.route('/api/labels')
    def get_labels():
        labels = store.session.query(Label).filter(Label.active == True).all()
        labelnames = [label.name for label in labels]
        return {'data': labelnames}

    @app.route('/api/search/<id>/<page>/results', methods=['GET'])
    def get_search_results(id, page):
        page = int(page)
        requester = get_requesting_user()
        if requester is None:
            raise Unauthorized()
        elif not is_integer(id):
            raise BadRequest()
        else:
            search = store.session.query(Search).filter_by(id=id).first()
            if search is None:
                raise NotFound()
            else:
                if search.has_admin_rights(requester):
                    matching_searches = search_utils.find_matching_searches(search, page)

                    serialized = [
                        search.serialize(
                            requester,
                            exclude=[],
                        ) for search in matching_searches
                    ]
                    response = {'data': serialized}
                else:
                    raise Forbidden()
        return response
