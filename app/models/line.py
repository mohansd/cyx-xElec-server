# -*- coding: utf-8 -*-

from .base import Base
from .load_type import LoadType
from mongoengine import StringField, IntField, ObjectIdField, BooleanField, FloatField


class Line(Base):
    """
    设备线路
    """
    line = IntField(choices=(0, 1, 2, 3, 4), required=True)
    line_name = StringField(required=True)  # 默认名
    device_id = StringField(required=True)
    choice_plan = ObjectIdField()
    plan_status = BooleanField()
    limit = FloatField(required=True)  # 电流容量
    standard = IntField(required=True)  # 电流阈值(默认78)
    load_type_id = ObjectIdField()
    meta = {
        'collection': 'line',
        'strict': True
    }

    def keys(self):
        self.append('load_type')
        return self.fields

    @property
    def load_type(self):
        if self.load_type_id:
            load_type = LoadType.get(id=self.load_type_id)
            return load_type.load_type
        else:
            return "未选择"
