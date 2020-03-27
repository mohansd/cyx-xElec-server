# _*_ coding: utf-8 _*_
"""

"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.validators.base import BaseValidator


class CreateAgentValidator(BaseValidator):
    username = StringField(validators=[DataRequired(message='账号名不能为空')])
    realname = StringField()
    password = StringField(default='123456')
    mobile = StringField(validators=[
        length(min=11, max=11, message='手机号为11个数字'),
        Regexp(r'^1(3|4|5|7|8)[0-9]\d{8}$')
    ])
    email = StringField(validators=[Email(message='无效email')])
    company_name = StringField()


class UpdateAgentValidator(BaseValidator):
    username = StringField()
    realname = StringField()
    mobile = StringField(validators=[
        length(min=11, max=11, message='手机号为11个数字'),
        Regexp(r'^1(3|4|5|7|8)[0-9]\d{8}$')
    ])
    email = StringField(validators=[Email(message='无效email')])
    company_name = StringField()