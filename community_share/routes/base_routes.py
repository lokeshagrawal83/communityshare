import logging
from functools import wraps

from flask import jsonify, request, Blueprint

from sqlalchemy.exc import IntegrityError, InvalidRequestError

from community_share import store
from community_share.utils import StatusCodes, is_integer
from community_share.authorization import get_requesting_user
from community_share.models.base import ValidationException


def make_not_authorized_response():
    response_data = {'message': 'Authorization failed'}
    response = jsonify(response_data)
    response.status_code = StatusCodes.NOT_AUTHORIZED
    return response


def make_forbidden_response():
    response_data = {'message': 'Forbidden'}
    response = jsonify(response_data)
    response.status_code = StatusCodes.FORBIDDEN
    return response


def make_not_found_response():
    response_data = {'message': 'Not found'}
    response = jsonify(response_data)
    response.status_code = StatusCodes.NOT_FOUND
    return response


def make_bad_request_response(message=None):
    if message is None:
        message = 'Bad request'
    response_data = {'message': message}
    response = jsonify(response_data)
    response.status_code = StatusCodes.BAD_REQUEST
    return response


def make_OK_response(message=None):
    if message is None:
        message = 'OK'
    response_data = {'message': message}
    response = jsonify(response_data)
    response.status_code = StatusCodes.OK
    return response


def make_server_error_response(message=None):
    if message is None:
        message = 'Server error'
    response_data = {'message': message}
    response = jsonify(response_data)
    response.status_code = StatusCodes.SERVER_ERROR
    return response


def make_many_response(requester, items):
    serialized = [item.serialize(requester) for item in items]
    serialized = [s for s in serialized if s is not None]
    response_data = {'data': serialized}
    response = jsonify(response_data)
    return response


def make_single_response(requester, item, include_user=None):
    '''
    Sometimes we want to include the current user info in the response
    since it might be changed by a request.
    '''
    if item is None:
        response = make_not_found_response()
    else:
        serialized = item.serialize(requester)
        if serialized is None:
            response = make_forbidden_response()
        else:
            response_data = {'data': serialized}
            if include_user is not None:
                serialized_user = include_user.serialize(requester)
                response_data['user'] = serialized_user
            response = jsonify(response_data)
    return response


def get_items(base_class, request=request):
    requester = get_requesting_user()
    if requester is None and not base_class.PERMISSIONS.get('all_can_read_many', False):
        response = make_not_authorized_response()
    else:
        if requester is None or not requester.is_administrator:
            if (base_class.PERMISSIONS.get('standard_can_read_many', False) or
                base_class.PERMISSIONS.get('all_can_read_many', False)):
                try:
                    query = base_class.args_to_query(request.args, requester)
                    if query is None:
                        response = make_forbidden_response()
                    else:
                        items = query.all()
                        response = make_many_response(requester, items)
                except ValueError as e:
                    error_message = ', '.join(e.args)
                    response = make_bad_request_response(e.args[0])
            else:
                response = make_forbidden_response()
        else:
            try:
                query = base_class.args_to_query(request.args, requester)
                items = query.all()
                response = make_many_response(requester, items)
            except ValueError as e:
                error_message = ', '.join(e.args)
                response = make_bad_request_response(e.args[0])
    return response


def get_item(id, base_class):
    requester = get_requesting_user()
    if requester is None:
        response = make_not_authorized_response()
    elif not is_integer(id):
        response = make_bad_request_response()
    else:
        item = store.session.query(base_class).filter_by(id=id, active=True).first()
        if item is None:
            response = make_not_found_response()
        else:
            response = make_single_response(requester, item)
    return response


def add_item(base_class, request=request):
    requester = get_requesting_user()
    data = request.json
    if not base_class.has_add_rights(data, requester):
        if requester is None:
            response = make_not_authorized_response()
        else:
            response = make_forbidden_response()
    else:
        try:
            item = base_class.admin_deserialize_add(data)
            store.session.add(item)
            store.session.commit()
            refreshed_item = store.session.query(base_class).filter_by(id=item.id).first()
            refreshed_item.on_add(requester)
            # commit again in case on_add changed it.
            store.session.commit()
            # and refresh again to update relationships
            refreshed_item = store.session.query(base_class).filter_by(id=item.id).first()
            response = make_single_response(requester, refreshed_item, include_user=requester)
        except ValidationException as e:
            response = make_bad_request_response(str(e))
        except (IntegrityError, InvalidRequestError) as e:
            if len(e.args) > 0:
                message = e.args[0]
            else:
                message = ''
            response = make_bad_request_response(message)
    return response


def edit_item(id, base_class, request=request):
    requester = get_requesting_user()
    if requester is None:
        response = make_not_authorized_response()
    elif not is_integer(id):
        response = make_bad_request_response()
    else:
        id = int(id)
        data = request.json
        data_id = data.get('id', None)
        if data_id is not None and int(data_id) != id:
            response = make_bad_request_response()
        else:
            if id is None:
                item = None
            else:
                item = store.session.query(base_class).filter_by(id=id).first()
            if item is None:
                response = make_not_found_response()
            else:
                if item.has_admin_rights(requester):
                    try:
                        item.admin_deserialize_update(data)
                        store.session.add(item)
                        item.on_edit(requester, unchanged=not store.session.dirty)
                        store.session.commit()
                        response = make_single_response(requester, item)
                    except ValidationException as e:
                        response = make_bad_request_response(str(e))
                else:
                    response = make_forbidden_response()
    return response


def delete_item(id, base_class):
    requester = get_requesting_user()
    if requester is None:
        response = make_not_authorized_response()
    elif not is_integer(id):
        response = make_bad_request_response()
    else:
        id = int(id)
        item = store.session.query(base_class).filter_by(id=id).first()
        if item is None:
            response = make_not_found_response()
        else:
            if item.has_delete_rights(requester):
                item.delete(requester)
                store.session.commit()
                response = make_single_response(requester, item)
            else:
                response = make_forbidden_response()
    return response


API_MANY_FORMAT = '/api/{0}'
API_SINGLE_FORMAT = '/api/{0}/<id>'
API_PAGINATION_FORMAT = '/api/{0}/<id>/<page>'


def make_blueprint(base_class, resource_name):

    api = Blueprint(resource_name, __name__)

    def inject_base_class(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            actual_base_class = kwargs.pop('base_class', base_class)
            return f(*args, base_class=actual_base_class, **kwargs)
        return wrapped

    api.route(
        API_MANY_FORMAT.format(resource_name),
        endpoint='get_many_{}'.format(resource_name),
        methods=['GET'],
    )(inject_base_class(get_items))

    api.route(
        API_SINGLE_FORMAT.format(resource_name),
        endpoint='get_{}'.format(resource_name),
        methods=['GET'],
    )(inject_base_class(get_item))

    api.route(
        API_MANY_FORMAT.format(resource_name),
        endpoint='add_{}'.format(resource_name),
        methods=['POST'],
    )(inject_base_class(add_item))

    api.route(
        API_SINGLE_FORMAT.format(resource_name),
        endpoint='edit_{}'.format(resource_name),
        methods=['PATCH', 'PUT'],
    )(inject_base_class(edit_item))

    api.route(
        API_SINGLE_FORMAT.format(resource_name),
        endpoint='delete_{}'.format(resource_name),
        methods=['DELETE'],
    )(inject_base_class(delete_item))

    return api
