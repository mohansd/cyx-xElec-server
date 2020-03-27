# _*_ coding: utf-8 _*_
from .base import Base
from mongoengine import StringField, IntField, ListField, FloatField


class DeviceCategory(Base):
    """
      设备类型(按照规格化分)
      与设备的关系是一对多
    """
    name = StringField(unique=True, required=True)  # 规格的类别名
    specs = ListField()  # 容量规格
    total_capacity = IntField()  # 总容量(单位: A)
    elec_limit = FloatField()  # 电流阈值
    warranty_year = IntField(default=0)  # 保证年限(单位: 年)

    meta = {
        'collection': 'device_category',
        'strict': True
    }
