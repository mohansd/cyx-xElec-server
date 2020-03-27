# _*_ coding: utf-8 _*_
from flask import request
from wtforms import FileField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError, NumberRange

from app.validators.base import BaseValidator


class UploadExcelValidator(BaseValidator):
    # ref==> https://wtforms.readthedocs.io/en/latest/fields.html
    file = FileField()

    def validate_file(self, value):
        self.file.data = request.files[value.name]