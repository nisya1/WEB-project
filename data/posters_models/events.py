import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Events(SqlAlchemyBase):
    __tablename__ = 'Events'

    EventId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    Title = sqla.Column(sqla.String, nullable=False)
    GenreId = sqla.Column(sqla.Integer, sqla.ForeignKey('EventGenre.GenreId'), nullable=False)
    TypeId = sqla.Column(sqla.Integer, sqla.ForeignKey('EventType.TypeId'), nullable=False)
    Rating = sqla.Column(sqla.Numeric, default=0, nullable=False)
    Duration = sqla.Column(sqla.String, default='00:00', nullable=False)
    ImageBlob = sqla.Column(sqla.BLOB, default=True)
    ImageName = sqla.Column(sqla.Text, default=True)
    Seats = sqla.Column(sqla.Integer, default=0, nullable=False)
    Price = sqla.Column(sqla.Integer, default=0, nullable=False)
    Time = sqla.Column(sqla.Text, nullable=False)
    # event = orm.relationship('User')

    def __repr__(self):
        return f'{self.Title}'
