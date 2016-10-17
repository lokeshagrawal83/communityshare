from flask import Response

from community_share.api.users.get_user import endpoint as get_user_endpoint
from community_share.flask_helpers import needs_auth
from community_share.models.user import User


@needs_auth()
def endpoint(requester: User) -> Response:
    """ Me Endpoint

    http:get:: /rest/me

    **Example request**:

    .. sourcecode:: http

       GET /rest/me HTTP/1.1
       Host: app.communityshare.us
       Accept: application/json
       Authorization: Basic:username:password

    **Example response**:

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
          "user": {
             "id": 23,
             "name": "Bob Smith",
             "bio": "On the weekends I polish copper mines."
          },
          "links": [ {
             "rel": "self",
             "href": "https://app.communityshare.us/rest/users/42"
          }
       }

    :query list string field: additional fields to return, always returns user id, default returns all fields

    :statuscode 200: user successfully fetched
    :statuscode 400: invalid arguments passed in
    :statuscode 401: needs authentication

    """
    return get_user_endpoint(user_id=requester.id)
