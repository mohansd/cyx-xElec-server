# -*- coding: utf-8 -*-
from app.models.line import Line
from app.models.device import Device
from app.models.alarm import Alarm


class AlarmService:
    def __init__(self, device_id, alarm_type, line_id=None, **kwargs):
        self.device_id = device_id
        self.line_id = line_id
        self.alarm_type = alarm_type
        self.detail = dict(kwargs)
        if line_id is not None:
            self.line = Line.objects.filter(id=line_id).first()
        self.device = Device.objects.filter(device_id=device_id).first()

    def gen_alarm(self):
        if self.alarm_type == "overload":
            self.overload_alarm()
        elif self.alarm_type == "trip":
            self.trip_alarm()
        elif self.alarm_type == "offline":
            self.offline_alarm()
        elif self.alarm_type == "high_current":
            self.high_current_alarm()
        elif self.alarm_type == "operate":
            self.operate_alarm()
        else:
            self.switch_alarm()

    def overload_alarm(self):
        level = 4
        message = self.device.alias + "配电柜, " + self.line.line_name + "线路, " + "电流值 " + "la:" + str(
            self.detail["a"]) + " lb:" + str(self.detail["b"]) + " lc:" + str(self.detail["c"]) + ", 线路过载"
        Alarm.generate_alarm(self.device_id, self.line_id, self.line.line, level, message, alarm_type="overload")

    def trip_alarm(self):
        level = 3
        message = self.device.alias + "配电柜, " + self.line.line_name + "线路, " + "跳闸"
        Alarm.generate_alarm(self.device_id, self.line_id, self.line.line, level, message, alarm_type="trip")

    def offline_alarm(self):
        level = 3
        message = self.device.alias + "配电柜离线"
        Alarm.generate_alarm(self.device_id, None, None, level, message, alarm_type="offline")

    def high_current_alarm(self):
        level = 2
        message = self.device.alias + "配电柜, " + self.line.line_name + "线路, " + "电流值 " + "la:" + str(
            self.detail["a"]) + " lb:" + str(self.detail["b"]) + " lc:" + str(self.detail["c"]) + ", 超过限定值: " + str(
            self.detail["limit"]) + "A"
        Alarm.generate_alarm(self.device_id, self.line_id, self.line.line, level, message, alarm_type="high_current")

    def switch_alarm(self):
        level = 1
        if self.detail["type"] == "on":
            operate = "从断电切换到通电"
        else:
            operate = "从通电切换到断电"
        print("this is line")
        print(type(self.line.line))
        message = self.device.alias + "配电柜, " + self.line.line_name + operate
        Alarm.generate_alarm(self.device_id, self.line_id, self.line.line, level, message, alarm_type="switch")

    def operate_alarm(self):
        pass

