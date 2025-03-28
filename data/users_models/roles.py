import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Roles(SqlAlchemyBase):
    __tablename__ = 'Roles'

    RoleId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    RoleName = sqla.Column(sqla.String, nullable=False, unique=True)
    users = orm.relationship('Users', backref='role')

    def __repr__(self):
        return f'<Role {self.RoleName}>'
