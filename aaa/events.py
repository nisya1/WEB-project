import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Events(SqlAlchemyBase):
    __tablename__ = 'Events'

    EventId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    GenreId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    TypeId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Rating = sqlalchemy.Column(sqlalchemy.NUMERIC, default=datetime.datetime.now)
    Duration = sqlalchemy.Column(sqlalchemy.String, default=datetime.datetime.now)
    Image = sqlalchemy.Column(sqlalchemy.BLOB, default=True)
    # event = orm.relationship('User')

    def __repr__(self):
        return f'<J> {self.job}'
