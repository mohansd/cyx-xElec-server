# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import StringField, DecimalField


class Anomaly(Base):
    """
    电流异常数据表
    """
    device_id = StringField()  # 设备Id
    normal = DecimalField()  # 阈值
    anomaly = DecimalField()  # 异常值
    diff = StringField()  # 差值，可以是一个百分比
    meta = {
        'collection': 'anomaly',
        'strict': True
    }
