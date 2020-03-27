# _*_ coding: utf-8 _*_
from wtforms import StringField, IntegerField, FileField, MultipleFileField
from wtforms.validators import DataRequired, AnyOf, length, Email, Regexp, ValidationError

from app.validators.base import BaseValidator
from app.libs.enums import ScopeEnum


class CDKeyValidator(BaseValidator):
    cdkey = StringField(validators=[DataRequired(message='激活码不能为空')])


class UpdateCDKeyValidator(CDKeyValidator):
    state = IntegerField(default=0)

    def validate_state(self, value):
        self.state.data = int(value.data)


class CreateCDKeyValidator(BaseValidator):
    # auth = IntegerField(validators=[AnyOf(values=[ScopeEnum.CO_ADMIN.value,
    #                                               ScopeEnum.CO_PROJECT.value,
    #                                               ScopeEnum.CO_OPERATE.value,
    #                                               ScopeEnum.CO_USER.value],
    #                                       message='不在授权范围内')
    #                                 ],
    #                     default=ScopeEnum.CO_USER.value)
    company_id = StringField(validators=[DataRequired(message='公司ID不能为空')])
    project_id = StringField()  # 可以为空
    group_id = StringField()
