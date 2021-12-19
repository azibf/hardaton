import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from . import db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronimic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pressure = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    pulse = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    temperature = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    reaction = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    sobriety = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    work_experience = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    driver_license = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    doctor_comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True, default='')
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True, default='')
    is_ready = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=0)
    doctor_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    is_doctor = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=1)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
