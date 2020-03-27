# -*- coding: utf-8 -*-
from mongoengine import StringField, IntField, BooleanField
from .base import Base


class Operation(Base):
    """
    操作记录表
    """
    user_id = StringField()  # 用户ID
    action = IntField()  # 1为通电操作，0为断电操作
    success = BooleanField()  # 操作结果
    meta = {
        'collection': 'operation',
        'strict': True
    }
