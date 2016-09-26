from typing import Any, Dict, List, Tuple

from iso8601 import parse_date

from flask import jsonify, request, Response

from sqlalchemy import true, false

from community_share import Store
from community_share.app_exceptions import BadRequest
from community_share.flask_helpers import api_path, needs_auth, serialize_many, with_store
from community_share.models.institution import Institution, InstitutionAssociation
from community_share.models.user import User
from community_share.utils import clamped, int_or


@needs_auth()
def endpoint(requester: User) -> Response:
    """ Users Endpoint

    http:get:: /rest/users/

    **Example request**:

    .. sourcecode:: http

       GET /rest/users?field=name&field=bio&match_any=name:Bob&match_any=name:Alice HTTP/1.1
       Host: app.communityshare.us
       Accept: application/json
       Authorization: Basic:username:password

    **Example response**:

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
          "count": 2,
          "users": [ {
             "id": 23,
             "name": "Bob Smith",
             "bio": "On the weekends I polish copper mines.",
             "links": [ {
                "rel": "self",
                "href": "https://app.communityshare.us/rest/users/23"
             } ]
          }, {
             "id": 42,
             "name": "Alice Jones",
             "bio": "In college I broke the record for underwater basket-weaving.",
             "links": [ {
                "rel": "self",
                "href": "https://app.communityshare.us/rest/users/42"
             } ]
          } ],
          "links": [ {
             "rel": "self",
             "href": "https://app.communityshare.us/rest/users/?number=10&offset=0&field=name&field=bio&search=name:Bob&search=name:Alice"
          }, {
             "rel": "next_page",
             "href": "https://app.communityshare.us/rest/users/?number=10&offset=10&field=name&field=bio&search=name:Bob&search=name:Alice"
          }, {
             "rel": "prev_page",
             "href": "https://app.communityshare.us/rest/users/?number=10&offset=0&field=name&field=bio&search=name:Bob&search=name:Alice"
          } ]
       }

    :query int number: maximum number of returned results, default is 10, max is 100
    :query int offset: offset into results to retrieve, default is 0

    :query list string field: additional fields to return, always returns user id
    :query list string match_any: field:value pairs sought in search joined as 'or'
    :query list string match_all: field:value pairs required in search joined as 'and'

    :statuscode 200: search successful
    :statuscode 400: invalid arguments passed in
    :statuscode 401: needs authentication

    :>json number count: total number of results in database for search

    """
    number = clamped(1, 100, int_or(request.args.get('number'), 10))
    offset = max(0, int_or(request.args.get('offset'), 0))
    fields = request.args.getlist('field')
    matches_all = parse_matches(request.args.getlist('matches_all'), 'matches_all')
    matches_any = parse_matches(request.args.getlist('matches_any'), 'matches_any')

    users, count = get_users(
        number=number,
        offset=offset,
        matches_all=matches_all,
        matches_any=matches_any,
    )
    users = serialize_many(requester, users, fields=fields)

    next_offset = offset if count <= offset + number else offset + number

    return jsonify({
        'count': count,
        'users': [
            {
                **user,
                'links': [{
                    'rel': 'self',
                    'href': api_path('users/{}'.format(user['id'])),
                }]
            } for user in users
        ],
        'links': [
            {
                'rel': 'self',
                'href': request.url,
            },
            {
                'rel': 'prev_page',
                'href': api_path('users', {
                    **request.args.to_dict(flat=False),
                    'number': number,
                    'offset': max(0, offset - number),
                })
            },
            {
                'rel': 'next_page',
                'href': api_path('users', {
                    **request.args.to_dict(flat=False),
                    'number': number,
                    'offset': next_offset,
                })
            }
        ]
    })


@with_store
def get_users(
    number: int=10,
    offset: int=0,
    matches_all: Dict[str, Any]={},
    matches_any: Dict[str, Any]={},
    store: Store=None,
) -> Tuple[List[User], int]:
    query = store.session.query(User)
    query = query.outerjoin(InstitutionAssociation)
    query = query.outerjoin(Institution)
    query = query.order_by(User.id.asc())

    searches = {
        'bio': lambda a: User.bio.ilike('%{}%'.format(a)),
        'created_after': lambda a: User.date_created > a,
        'created_before': lambda a: User.date_created < a,
        'institution': lambda a: Institution.name.ilike('%{}%'.format(a)),
        'name': lambda a: User.name.ilike('%{}%'.format(a)),
    }

    filter_all = true()
    filter_any = false()

    for name, value in matches_all.items():
        filter_all = filter_all & searches.get(name, lambda _: true())(value)

    for name, value in matches_any.items():
        filter_any = filter_any | searches.get(name, lambda _: false())(value)

    query = query.filter(filter_all & filter_any if filter_any is not false() else filter_all)
    query = query.distinct()
    count = query.count()
    query = query.limit(number).offset(offset)

    return query, count


def parse_match(match: str, match_type: str) -> Tuple[str, Any]:
    try:
        key, value = match.split(':', 1)
    except:
        raise BadRequest(
            'Invalid match field given: {}={}\n'
            'Match requirements should be passed in as name:value\n'
            'For example, to search for users with a name containing "Josh"\n'
            'Pass in `matches_any=name:Josh` or `matches_all=name:Josh`'
                .format(match_type, match)
        )

    if key in {'created_after', 'created_before'}:
        try:
            return key, parse_date(value)
        except:
            raise BadRequest(
                'Could not parse date field: {}={}\n'
                'Dates should be passed in ISO8601 format\n'
                'For example, to search for users created after January 15, 2016\n'
                'Pass in `matches_all=created_after:2016-01-15T16:29:58-07:00'
                    .format(match_type, match)
            )

    return key, value


def parse_matches(matches: List[str], match_type: str) -> Dict[str, Any]:
    return dict(parse_match(match, match_type) for match in matches)
