# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/26.
"""
from mongoengine import IntField, StringField, ObjectIdField
from app.models.base import Base

__author__ = 'Allen7D'


class Auth(Base):
    """
    权限表
    """
    group_id = ObjectIdField() # 所属权限组id
    auth = StringField() # 权限字段
    module = StringField # 权限的模块

