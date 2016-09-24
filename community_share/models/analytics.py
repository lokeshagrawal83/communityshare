from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from community_share import Base
from community_share.models.user import User


class PageView(Base):
    __tablename__ = 'page_views'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey(User.id))
    viewed_at = Column('viewed_at', DateTime, default=datetime.utcnow)
    next_path = Column('next_path', String(255))
    prev_path = Column('prev_path', String(255))

    def __init__(self, user_id, next_path, prev_path):
        self.user_id = user_id
        self.viewed_at = datetime.utcnow()
        self.next_path = next_path
        self.prev_path = prev_path

    def __repr__(self):
        return '<PageView(user_id={},time={},to={},from={})>'.format(
            self.user_id,
            self.viewed_at,
            self.next_path,
            self.prev_path,
        )
