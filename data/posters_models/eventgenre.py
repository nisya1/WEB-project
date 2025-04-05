import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class EventGenre(SqlAlchemyBase):
    __tablename__ = 'EventGenre'

    GenreId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    GenreName = sqla.Column(sqla.String, nullable=False, unique=True)
    # event = orm.relationship('User')

    def __repr__(self):
        return f'{self.GenreName}'
