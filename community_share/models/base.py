import logging
import datetime
import dateutil
from dateutil import parser
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, String, DateTime, Boolean

from community_share import Base, store

logger = logging.getLogger(__name__)


class ValidationException(Exception):
    pass


class Serializable(object):
    """
    Doesn't implement a necessary 'get' method.
    """

    MANDATORY_FIELDS = []
    WRITEABLE_ONCE_FIELDS = []
    WRITEABLE_FIELDS = []
    STANDARD_READABLE_FIELDS = ['id']
    ADMIN_READABLE_FIELDS = ['id']

    PERMISSIONS = {
        'all_can_read_many': False,
        'standard_can_read_many': False,
        'admin_can_delete': False
    }

    @classmethod
    def has_add_rights(cls, data, requester):
        return (requester is not None and requester.is_administrator)

    def has_standard_rights(self, requester):
        has_rights = False
        if requester is not None:
            has_rights = True
        return has_rights

    def has_admin_rights(self, requester):
        return (requester is not None and requester.is_administrator)

    def has_delete_rights(self, requester):
        has_rights = False
        if requester is not None:
            if requester.is_administrator:
                has_rights = True
            elif (self.PERMISSIONS['admin_can_delete'] and self.has_admin_rights(requester)):
                has_rights = True
        return has_rights

    custom_serializers = {}

    def serialize(self, requester, exclude: List[str] = []) -> Optional[Dict[str, Any]]:
        """
        Serializes readable fields by user role

        :param requester: user requesting data
        :param exclude: optional list of fields by name to exclude
        :return: readable fields for user or None if no permission
        """
        if self.has_admin_rights(requester):
            fieldnames = self.ADMIN_READABLE_FIELDS
        elif self.has_standard_rights(requester):
            fieldnames = self.STANDARD_READABLE_FIELDS
        else:
            return None

        return {
            key: (
                self.custom_serializers[key](self, requester)
                if key in self.custom_serializers else getattr(self, key)
            )
            for key in (set(fieldnames) - set(exclude)) | ({'id'} if hasattr(self, 'id') else set())
        }

    def delete(self, requester):
        previously_deleted = not self.active
        if not previously_deleted:
            self.active = False
            store.session.add(self)
            self.on_delete(requester)

    def on_delete(self, requester):
        pass

    def on_add(self, requester):
        pass

    def on_edit(self, requester, unchanged=False):
        pass

    custom_deserializers = {}

    @classmethod
    def admin_deserialize_add(cls, data):
        for fieldname in cls.MANDATORY_FIELDS:
            if not fieldname in data:
                raise ValidationException('Missing necessary field: {0}'.format(fieldname))
        item = cls()
        item.admin_deserialize_update(data, add=True)
        return item

    def admin_deserialize_update(self, data, add=False):
        logger.debug('admin_deserialize_update')
        if add:
            fieldnames = (
                set(self.MANDATORY_FIELDS) |
                set(self.WRITEABLE_FIELDS) |
                set(self.WRITEABLE_ONCE_FIELDS)
            ) # yapf: disable
        else:
            fieldnames = self.WRITEABLE_FIELDS
        for fieldname in data.keys():
            logger.debug('fieldname is {}'.format(fieldname))
            if fieldname in self.custom_deserializers:
                value = data.get(fieldname, None)
                self.custom_deserializers[fieldname](self, value)
            elif fieldname in fieldnames and hasattr(self, fieldname):
                current = getattr(self, fieldname)
                # Force type conversion of datetime beforehand so sqlalchemy doesn't
                # falsely label things as dirty.
                new_value = data[fieldname]
                if type(current) == datetime.datetime:
                    new_value = dateutil.parser.parse(data[fieldname])
                    new_value = new_value.replace(tzinfo=None)
                if current != new_value:
                    message = '{0} - changing attr from {1} to {2}'
                    logger.debug(message.format(fieldname, current, data[fieldname]))
                    setattr(self, fieldname, data[fieldname])

    @classmethod
    def admin_deserialize(cls, data):
        item_id = data.get('id', None)
        if item_id is not None:
            item = store.session.query(cls).filter(cls.id == data['id']).first()
            if item is not None:
                item.admin_deserialize_update(data)
        else:
            item = cls.admin_deserialize_add(data)
        return item

    CONDITION_MAPPING = {
        'greaterthanorequal': lambda x, y: (x >= y),
        'greaterthan': lambda x, y: (x > y),
        'lessthanorequal': lambda x, y: (x <= y),
        'lessthan': lambda x, y: (x < y),
    }

    @classmethod
    def _args_to_filter_params(cls, args):
        filter_args = [(cls.active == True)]
        for key in args.keys():
            bits = key.split('.')
            if hasattr(cls, bits[0]):
                if len(bits) > 2:
                    raise Exception('Unknown filter parameter')
                elif len(bits) == 2:
                    if bits[1] in ('like', 'ilike'):
                        if args[key]:
                            new_arg = getattr(getattr(cls, bits[0]), bits[1])(args[key])
                            filter_args.append(new_arg)
                    elif bits[1] in ('in', ):
                        if args.getlist(key):
                            new_arg = getattr(cls, bits[0]).in_(args.getlist(key))
                            filter_args.append(new_arg)
                    elif bits[1] in cls.CONDITION_MAPPING.keys():
                        if args[key]:
                            field = getattr(cls, bits[0])
                            value = args[key]
                            condition = cls.CONDITION_MAPPING[bits[1]](field, value)
                            filter_args.append(condition)
                    else:
                        raise Exception('Unknown filter parameter')
                elif len(bits) == 1:
                    typ = getattr(cls, key).property.columns[0].type
                    value = args[key]
                    if (isinstance(typ, Boolean)):
                        if (value == 'true'):
                            value = True
                        elif (value == 'false'):
                            value = False
                    criterium = (getattr(cls, key) == value)
                    filter_args.append(criterium)
        return filter_args

    @classmethod
    def _args_to_query(cls, args, requester=None):
        filter_args = cls._args_to_filter_params(args)
        query = store.session.query(cls).filter(*filter_args)
        return query

    @classmethod
    def args_to_query(cls, args, requester=None):
        query = cls._args_to_query(args, requester)
        return query
