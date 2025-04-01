import sqlalchemy as sqla
from sqlalchemy import orm
from data.users_models.roles import Roles

from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'Users'

    UserId = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    Name = sqla.Column(sqla.String, nullable=False, unique=True)
    RoleId = sqla.Column(sqla.Integer, sqla.ForeignKey('Roles.RoleId'), nullable=False, default=2)
    Email = sqla.Column(sqla.String, nullable=False, unique=True)
    Password = sqla.Column(sqla.String, nullable=False)

    def __repr__(self):
        return f'<User {self.Name}>'
