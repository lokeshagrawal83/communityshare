import logging

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from community_share import Base, store
from community_share.models.base import Serializable, ValidationException

logger = logging.getLogger(__name__)


class InstitutionAssociation(Base, Serializable):
    __tablename__ = 'institution_association'

    MANDATORY_FIELDS = ['role']
    WRITEABLE_FIELDS = ['role']
    STANDARD_READABLE_FIELDS = ['role', 'institution']
    ADMIN_READABLE_FIELDS = ['role', 'institution']

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    institution_id = Column(Integer, ForeignKey('institution.id'), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    role = Column(String(100), nullable=False)
    unique_constraint = UniqueConstraint('user_id', 'institution_id')

    user = relationship('User')
    institution = relationship('Institution')

    def deserialize_institution(self, data):
        name = data.get('name', None)
        institution_type = data.get('institution_type', None)
        institution = None
        if name:
            self.institution = store.session.query(Institution).filter_by(name=name).first()
        if not self.institution:
            if len(name) > INSTITUTION_NAME_LENGTH:
                error_message = 'Institution name must be less than {} characters.'
                raise ValidationException(error_message.format(INSTITUTION_NAME_LENGTH))
            else:
                self.institution = Institution.admin_deserialize_add(data)
        else:
            self.institution.institution_type = institution_type

    def serialize_institution(self, requester):
        return self.institution.serialize(requester)

    custom_deserializers = {'institution': deserialize_institution}

    custom_serializers = {'institution': serialize_institution}


INSTITUTION_NAME_LENGTH = 50


class Institution(Base, Serializable):
    __tablename__ = 'institution'

    MANDATORY_FIELDS = ['name']
    WRITEABLE_FIELDS = ['name', 'institution_type']
    STANDARD_READABLE_FIELDS = ['name', 'institution_type']
    ADMIN_READABLE_FIELDS = ['name', 'institution_type']

    PERMISSIONS = {'all_can_read_many': True, 'standard_can_read_many': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(INSTITUTION_NAME_LENGTH), nullable=False, unique=True)
    institution_type = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    description = Column(String)

    def has_standard_rights(self, requester):
        return True
