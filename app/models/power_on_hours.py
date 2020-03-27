# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import ListField, DateTimeField, StringField


class PowerOnHours(Base):
    """
    记录设备通/断电时长表
    """
    device_id = StringField()  # 设备ID
    state = StringField()  # 通/断 电状态
    zero_point = DateTimeField()  # 当日0点时间戳
    time_bucket = ListField()  # 时间列表     [{"start":"end":}]
    meta = {
        'collection': 'powerOnHours',
        'strict': True
    }
