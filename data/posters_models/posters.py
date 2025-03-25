import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Events(SqlAlchemyBase):
    __tablename__ = 'Events'

    PosterId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    EventId = sqla.Column(sqla.Integer, sqla.ForeignKey('Events.EventId'), nullable=False)
    LocationId = sqla.Column(sqla.Integer, sqla.ForeignKey('Locations.LocationId'), nullable=False)
    Seats = sqla.Column(sqla.Integer, default=0, nullable=False)
    Price = sqla.Column(sqla.Integer, default=0, nullable=False)
    Time = sqla.Column(sqla.Text, nullable=False)
    # event = orm.relationship('User')

    def __repr__(self):
        return f'{self.PosterId}'
