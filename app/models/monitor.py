# -*- coding: utf-8 -*-
from mongoengine import StringField, ObjectIdField, IntField, DynamicField
from .base import Base
from .line import Line
from .load_type import LoadType

class Monitor(Base):
    """
    采集数据表
    """
    device_id = StringField()  # 设备ID
    line_id = ObjectIdField()
    line = IntField()
    line_name = StringField()
    type = StringField()
    value = DynamicField()
    meta = {
        'collection': 'monitor',
        'strict': True,
        'ordering': ['-createdAt']
    }

    @staticmethod
    def save_data(data):
        monitor = Monitor()
        monitor.device_id = data["device_id"]
        monitor.line_id = data["line_id"]
        monitor.line = data["line"]
        monitor.type = data["type"]
        monitor.value = data["value"]
        monitor.save()

    @staticmethod
    def device_status(device_id, lines):
        types = ["energy", "voltage", "electricity", "status"]
        result = {}
        for line in lines:
            result[line.line] = {}
            for type in types:
                monitor = Monitor.objects.filter(device_id=device_id, line_id=line.id, type=type).first()
                if monitor:
                    result[line.line][type] = monitor.value
                else:
                    result[line.line][type] = None
            result[line.line]["line_name"] = line.line_name
            result[line.line]["load_type"] = line.load_type
            result[line.line]["load_type_id"] = line.load_type_id
            if line.load_type_id:
                load_type = LoadType.objects.filter(id=line.load_type_id).first()
                result[line.line]["load_type_detail"] = {
                    "power": load_type.power,
                    "electricity": load_type.electricity,
                    "voltage": load_type.voltage
                }
            else:
                result[line.line]["load_type_detail"] = {}
        return result
