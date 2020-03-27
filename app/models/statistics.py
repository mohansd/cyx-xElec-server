# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import StringField, DateTimeField, DynamicField, ObjectIdField


class Statistics(Base):
    """
    统计表
    """
    zero_point = DateTimeField()  # 当日零点时间
    date_type = StringField()  # day为日报表, month为月报表
    data_type = StringField()  # power为电能情况，break为跳闸次数,event为事件次数, analyze为分析
    device_id = StringField()
    line_id = ObjectIdField()
    value = DynamicField()
    meta = {
        'collection': 'statistics',
        'strict': True
    }
