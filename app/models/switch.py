# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import IntField, StringField


class SwitchState(Base):
    """
    跳闸记录表
    """
    device_id = StringField()
    company_name = StringField()
    action = IntField()  # 1为通电，0为断电
    meta = {
        'collection': 'switchstate',
        'strict': True
    }

