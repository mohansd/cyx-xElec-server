# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import StringField, IntField, ListField


class Message(Base):
    """
    推送信息表
    """
    type = StringField()  # 事件event, 计划plane, 天气weather, 报表statement
    message = StringField()  # 信息内容
    state = IntField()  # 1为已推送，0为未推送
    receiver = ListField()  # 接收者，为openid
    meta = {
        'collection': 'message',
        'strict': True
    }
