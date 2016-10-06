import logging

from flask import request, jsonify, make_response

from community_share.models.user import User, UserReview
from community_share.models.institution import Institution
from community_share.authorization import get_requesting_user
from community_share import mail_actions
from community_share.routes import base_routes
from community_share import store
from community_share.models.base import ValidationException
from community_share.picture_utils import image_to_user_filename, is_allowable_image, store_image

logger = logging.getLogger(__name__)


def register_user_routes(app):

    user_blueprint = base_routes.make_blueprint(User, 'user')
    app.register_blueprint(user_blueprint)

    user_review_blueprint = base_routes.make_blueprint(UserReview, 'user_review')
    app.register_blueprint(user_review_blueprint)

    institution_blueprint = base_routes.make_blueprint(Institution, 'institution')
    app.register_blueprint(institution_blueprint)

    @app.route('/api/usersignup', methods=['POST'])
    def usersignup():
        data = request.json
        user = data.get('user', None)
        email = user.get('email', '')
        password = data.get('password', None)
        # Check that the email isn't in use.
        existing_user = store.session.query(User)
        existing_user = existing_user.filter(User.email == email, User.active == True)
        existing_user = existing_user.first()
        if existing_user is not None:
            response = base_routes.make_bad_request_response(
                'That email address is already associated with an account.',
            )
        elif password is None:
            response = base_routes.make_bad_request_response('A password was not specified.')
        else:
            try:
                user = User.admin_deserialize_add(user)
                error_messages = user.set_password(password)
                if error_messages:
                    error_message = ', '.join(error_messages)
                    response = base_routes.make_bad_request_response(error_message)
                else:
                    store.session.add(user)
                    store.session.commit()
                    error_message = mail_actions.request_signup_email_confirmation(user)
                    secret = user.make_api_key()
                    serialized = user.serialize(user)
                    warning_message = 'Failed to send email confirmation: {0}'.format(error_message)
                    response_data = {
                        'data': serialized,
                        'apiKey': secret.key,
                        'warningMessage': warning_message,
                    }
                response = jsonify(response_data)
            except ValidationException as e:
                response = base_routes.make_bad_request_response(str(e))
        return response

    @app.route('/api/userbyemail/<string:email>', methods=['GET'])
    def userbyemail(email):
        requester = get_requesting_user()
        if requester is None:
            response = base_routes.make_not_authorized_response()
        elif requester.email != email:
            response = base_routes.make_forbidden_response()
        else:
            users = store.session.query(User).filter(User.email == email, User.active == True).all()
            if len(users) > 1:
                logger.error('More than one active user with the same email - {}'.format(email))
                user = users[0]
            elif len(users) == 0:
                user = None
            else:
                user = users[0]
            if user is None:
                response = base_routes.make_not_found_response()
            else:
                response = base_routes.make_single_response(requester, user)
        return response

    @app.route('/api/requestresetpassword/<string:email>', methods=['GET'])
    def request_reset_password(email):
        user = store.session.query(User).filter_by(email=email, active=True).first()
        if user is None:
            response = base_routes.make_not_found_response()
        else:
            error_message = mail_actions.request_password_reset(user)
            if error_message:
                response = base_routes.make_server_error_response(error_message)
            else:
                response = base_routes.make_OK_response()
        return response

    @app.route('/api/requestapikey', methods=['GET'])
    def request_api_key():
        requester = get_requesting_user()
        if requester is None:
            response = base_routes.make_not_authorized_response()
        else:
            secret = requester.make_api_key()
            response_data = {'apiKey': secret.key}
            response = jsonify(response_data)
        return response

    @app.route('/api/resetpassword', methods=['POST'])
    def reset_password():
        data = request.json
        key = data.get('key', '')
        password = data.get('password', '')
        if key == '':
            response = base_routes.make_bad_request_response(
                'Did not receive a key with password reset request.',
            )
        elif password == '':
            response = base_routes.make_bad_request_response(
                'Received password to reset to was blank.',
            )
        else:
            user, error_messages = mail_actions.process_password_reset(key, password)
            if error_messages:
                error_message = ', '.join(error_messages)
                response = base_routes.make_bad_request_response(error_message)
            elif user is None:
                response = base_routes.make_bad_request_response()
            else:
                response = base_routes.make_single_response(user, user)
        return response

    @app.route('/api/requestconfirmemail', methods=['GET'])
    def request_confirm_email():
        requester = get_requesting_user()
        if requester is None:
            response = base_routes.make_not_authorized_response()
        else:
            error_message = mail_actions.request_signup_email_confirmation(requester)
            if error_message:
                response = base_routes.make_server_error_response(error_message)
            else:
                response = base_routes.make_OK_response()
        return response

    @app.route('/api/confirmemail', methods=['POST'])
    def confirm_email():
        data = request.json
        key = data.get('key', '')
        if key == '':
            response = base_routes.make_bad_request_response(
                'Did not receive a key with email confirmation.',
            )
        else:
            user, error_messages = mail_actions.process_confirm_email(key)
            if error_messages:
                error_message = ', '.join(error_messages)
                response = base_routes.make_bad_request_response(error_message)
            elif user is None:
                response = base_routes.make_bad_request_response()
            else:
                secret = user.make_api_key()
                serialized = user.serialize(user)
                response_data = {
                    'data': serialized,
                    'apiKey': secret.key,
                }
                response = jsonify(response_data)
        return response

    @app.route('/api/usersearch', methods=['GET'])
    def search():
        requester = get_requesting_user()
        search_text = request.args.get('search_text', None)
        date_created_greaterthan = request.args.get('date_created.greaterthan', None)
        date_created_lessthan = request.args.get('date_created.lessthan', None)
        users = User.search(search_text, date_created_greaterthan, date_created_lessthan)
        response = base_routes.make_many_response(requester, users)
        return response

    @app.route('/api/user/<int:user_id>/picture', methods=['PUT', 'POST', 'PATCH'])
    def post_picture(user_id):
        user = get_requesting_user()

        if user_id != user.id:
            return base_routes.make_not_authorized_response()

        image_file = request.files['file']
        if not image_file:
            return base_routes.make_bad_request_response('missing image data')

        image_data = image_file.read()
        if not is_allowable_image(image_data):
            return base_routes.make_bad_request_response('unallowed image type')

        filename = image_to_user_filename(image_data, user_id)

        store_image(image_file, filename)

        user.picture_filename = filename
        store.session.add(user)
        store.session.commit()

        logger.info('Saving image {!r}'.format(filename))

        return base_routes.make_OK_response()

    @app.route('/api/activate_email', methods=['POST'])
    def activate_email():
        User.activate_email()

    @app.route('/api/dump_csv', methods=['GET'])
    def dump_csv():
        csv_obj = User.dump_csv()
        response = make_response(csv_obj.getvalue())
        response.headers["Content-Type"] = "text/csv"
        response.headers["Content-Disposition"] = "attachment; filename=communityshare.csv"
        return response
