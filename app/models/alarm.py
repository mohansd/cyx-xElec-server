# -*- coding: utf-8 -*-
from .base import Base
from .device import Device
from mongoengine import StringField, ObjectIdField, IntField, DictField


class Alarm(Base):
    alarm_type = StringField()
    device_id = StringField()  # 设备Id
    device_location = DictField()
    device_category = StringField()
    line_id = ObjectIdField()
    line = IntField()
    project_id = ObjectIdField()
    level = IntField()
    message = StringField()
    user_id = ObjectIdField()
    status = IntField(default=0)
    meta = {
        'collection': 'alarm',
        'strict': True
    }

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.exclude = ['updatedAt', '_cls']
        self.fields = list(set(self._fields_ordered) - set(self.exclude))

    @staticmethod
    def generate_alarm(device_id, line_id, line, level, message, alarm_type):
        alarm = Alarm()
        alarm["device_id"] = device_id
        if line_id is not None:
            alarm["line_id"] = line_id
            alarm["line"] = line
        alarm["level"] = level
        alarm["message"] = message
        device = Device.objects.filter(device_id=device_id).first()
        alarm["project_id"] = device.project_id
        alarm["alarm_type"] = alarm_type
        alarm["device_location"] = device.location if device.location != {} else None
        alarm.save()
