# -*- coding: utf-8 -*-

from .base import Base
from mongoengine import StringField, ObjectIdField, FloatField, IntField


class LoadType(Base):
    """
    负载类型
    """
    load_type = StringField()
    company_id = ObjectIdField()
    power = FloatField(required=True)
    electricity = FloatField()
    voltage = IntField()
    meta = {
        'collection': 'load_type',
        'strict': True
    }
