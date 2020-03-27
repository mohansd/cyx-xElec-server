# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/6/16.
"""
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError, NumberRange

from app.validators.base import BaseValidator

class IDMustBePositiveInt(BaseValidator):
	id = IntegerField(validators=[DataRequired()])

	def validate_id(self, value):
		id = value.data
		if not self.isPositiveInteger(id):
			raise ValidationError(message='ID 必须为正整数')
		self.id.data = id


class PaginateValidator(BaseValidator):
	page = IntegerField(NumberRange(min=1), default=1) # 当前页
	size = IntegerField(NumberRange(min=1, max=100), default=10) # 每页条目个数

	def validate_page(self, value):
		self.page.data = int(value.data)

	def validate_size(self, value):
		self.size.data = int(value.data)

