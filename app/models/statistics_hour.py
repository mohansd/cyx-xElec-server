# -*- coding: utf-8 -*-

from .base import Base
from mongoengine import DateTimeField, StringField, FloatField, ObjectIdField


class StatisticsHour(Base):
    zero_time = DateTimeField()
    hour_time = DateTimeField()
    device_id = StringField()
    line_id = ObjectIdField()
    energy = FloatField()

    meta = {
        'collection': 'statistics_hour',
        'strict': True
    }