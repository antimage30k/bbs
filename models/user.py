import hashlib

from sqlalchemy import Column, String, Text, UnicodeText

import config
from models.base_model import SQLMixin, db
from enum import Enum, auto
from sqlalchemy.dialects import mysql


class UserRole(Enum):
    admin = auto()
    normal = auto()
    guest = auto()


class User(SQLMixin, db.Model):
    __tablename__ = 'user'
    """
    User 是一个保存用户数据的 model
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/default.jpg')
    email = Column(String(50), nullable=False, default=config.test_mail)
    # 签名
    signature = Column(UnicodeText, nullable=True, default='这家伙很懒，什么个性签名都没有留下。')
    # 权限
    role = Column(mysql.ENUM('admin', 'normal', 'guest'), nullable=False, default=UserRole.normal.name)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        # print('register', form)
        if len(name) > 0 and User.one(username=name) is None:
            # 错误，只应该 commit 一次
            # u = User.new(form)
            # u.password = u.salted_password(pwd)
            # User.session.add(u)
            # User.session.commit()
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        # print('validate_login', form, query)
        return User.one(**query)
