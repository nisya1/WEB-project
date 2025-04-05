import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Images(SqlAlchemyBase):
    __tablename__ = 'Images'

    ImageId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    ImageBlob = sqla.Column(sqla.BLOB)
    # event = orm.relationship('User')

    def __repr__(self):
        return f'{self.ImageId}'