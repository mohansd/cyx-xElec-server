# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import StringField, ObjectIdField
from app.service.socketservice import TCPServer
from .device import Device
class Project(Base):
    """
    公司项目表
    """
    name = StringField()  # 项目名称
    user_id = StringField()  # 负责人ID
    company_name = StringField()  # 公司名称
    company_id = ObjectIdField()  # 公司ID
    meta = {
        'collection': 'project',
        'strict': True
    }

    @staticmethod
    def get_online_number(project_id):
        clients = TCPServer.get_instance().clients
        devices = list(Device.objects.filter(project_id=project_id).all())
        sum = 0
        for device in devices:
            if device["cloud_id"] in clients.keys():
                sum = sum + 1
        return sum