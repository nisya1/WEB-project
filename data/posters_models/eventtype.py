import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class EventType(SqlAlchemyBase):
    __tablename__ = 'EventType'

    TypeId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    TypeName = sqla.Column(sqla.String, nullable=False, unique=True)
    # event = orm.relationship('User')

    def __repr__(self):
        return f'{self.TypeName}'
