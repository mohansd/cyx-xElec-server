# -*- coding: utf-8 -*-

from .base import Base
from mongoengine import DateTimeField, StringField, FloatField, ObjectIdField, IntField


class EnergyAvg(Base):
    month_time = DateTimeField()
    hour = IntField()
    device_id = StringField()
    line_id = ObjectIdField()
    energy = FloatField()

    meta = {
        'collection': 'energy_avg',
        'strict': True
    }