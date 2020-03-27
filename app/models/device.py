# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import StringField, DateTimeField, IntField, ObjectIdField, DictField, DecimalField
from app.models.device_category import DeviceCategory
from app.service.socketservice import TCPServer


class Device(Base):
    """
    设备表
    """
    device_id = StringField()  # 设备ID
    cloud_id = StringField()  # 云ID
    category_id = ObjectIdField()  # 设备类型ID
    icc_id = StringField() # 物联网卡ICCID
    contract_no = StringField() # 合并编号
    delivery_time = DateTimeField()  # 出厂时间
    warranty = DateTimeField()  # 保修期
    company_name = StringField()  # 公司名
    company_id = ObjectIdField()  # 公司ID
    project_name = StringField()  # 项目名
    project_id = ObjectIdField()  # 项目ID
    alias = StringField()  # 设备别名
    location = DictField()  # 设备位置，省市区
    electricity = DecimalField()  # 电流阈值
    # 异常百分数
    meta = {
        'collection': 'device',
        'strict': True
    }

    def keys(self):
        self.append('category_name')
        return self.fields

    @property
    def category_name(self):
        category = DeviceCategory.get(id=self.category_id)
        return category.name if category else '无规格'

    @staticmethod
    def check_online(cloud_id):
        clients = TCPServer.get_instance().clients
        if cloud_id in clients.keys():
            return True
        else:
            return False
