# -*- coding: utf-8 -*-

from .base import Base
from mongoengine import StringField, ListField, ObjectIdField


class Plan(Base):
    """
    设备线路
    """
    plan_name = StringField()
    on = ListField()
    off = ListField()
    project_id = ObjectIdField()
    meta = {
        'collection': 'plan',
        'strict': True
    }
