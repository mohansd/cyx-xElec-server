# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/26.
"""

from mongoengine import IntField, StringField, ObjectIdField

from app.models.base import Base
from app.models.auth import Auth as AuthModel

__author__ = 'Allen7D'


class Group(Base):
    """
    权限表
    """
    name = StringField()  # 权限组名称
    info = StringField()  # 权限组描述

    @property
    def auth_list(self):
        return []
