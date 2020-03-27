# _*_ coding: utf-8 _*_
from wtforms import StringField, IntegerField, FileField, MultipleFileField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.error_code import DuplicateException
from app.models.company import Company
from app.validators.base import BaseValidator


class CreateCompanyValidator(BaseValidator):
    company_name = StringField(validators=[DataRequired(message='公司名不能为空')])

    def validate_company_name(self, value):
        # 公司名不能重复
        company = Company.objects.filter(name=value.data).first()
        if company:
            raise DuplicateException(msg='公司名已经注册')
        self.company_name.data = value.data


class EditCompanyValidator(BaseValidator):
    company_name = StringField(validators=[DataRequired(message='公司名不能为空')])

    def validate_company_name(self, value):
        # 公司名不能重复
        company = Company.objects.filter(name=value.data).first()
        if company:
            raise DuplicateException(msg='公司名已经注册 或 重复修改')
        self.company_name.data = value.data
