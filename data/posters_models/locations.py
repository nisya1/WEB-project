import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Events(SqlAlchemyBase):
    __tablename__ = 'Events'

    LocationId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    LocationName = sqla.Column(sqla.String, nullable=False, unique=True)
    LocationAddress = sqla.Column(sqla.String, nullable=False, unique=True)
    FullLocationName = sqla.Column(sqla.String, nullable=False, unique=True)
    # event = orm.relationship('User')

    def __repr__(self):
        return f'{self.LocationName}'
