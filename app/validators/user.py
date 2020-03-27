# _*_ coding: utf-8 _*_
from wtforms import StringField, IntegerField, FileField, MultipleFileField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.models.company import Company
from app.models.user import User
from app.validators.base import BaseValidator


class UserValidator(BaseValidator):
    uid = StringField(validators=[DataRequired(message='用户ID不能为空')])


class FilterUserValidator(BaseValidator):
    company_id = StringField()
    group_id = StringField()


class CreateUserValidator(BaseValidator):
    username = StringField(validators=[DataRequired(message='账号名不能为空')])
    realname = StringField()
    password = StringField(default='123456')
    mobile = StringField(validators=[
        length(min=11, max=11, message='手机号为11个数字'),
        Regexp(r'^1(3|4|5|7|8)[0-9]\d{8}$')
    ])
    email = StringField(validators=[Email(message='无效email')])
    # auth = IntegerField()  # 如果是企业超级管理员，则设为10
    group_id = StringField()
    company_id = StringField()
    company_name = StringField()  # 通过company_id查询

    def validate_company_id(self, value):
        company = Company.objects.filter(id=value.data).first_or_404(msg='公司id不存在')
        self.company_name.data = company.name
        return value.data

    # def validate_auth(self, value):
    #     # 判断用户的权限(唯一用在高级用户创造低级用户）
    #     if value.data:
    #         self.auth.data = int(value.data)
    #     else:
    #         self.auth.data = None


class UpdateUserValidator(BaseValidator):
    username = StringField(validators=[DataRequired(message='账号不能为空')])
    realname = StringField(validators=[DataRequired(message='姓名不能为空')])
    # password = StringField(validators=[DataRequired(message='密码不能为空')])
    mobile = StringField(validators=[
        length(min=11, max=11, message='手机号为11个数字'),
        Regexp(r'^1(3|4|5|7|8)[0-9]\d{8}$')
    ])
    email = StringField(validators=[Email(message='无效email')])
    # auth = IntegerField()  # 如果是企业超级管理员，则设为10

    # def validate_auth(self, value):
    #     # 判断用户的权限(唯一用在高级用户创造低级用户）
    #     if value.data:
    #         self.auth.data = int(value.data)
    #     else:
    #         self.auth.data = None
